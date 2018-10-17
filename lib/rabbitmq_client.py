import pika
import logging
import queue
from functools import partial
from json import dumps, loads
from sys import exit
import lib.config as config

mq_logger = logging.getLogger("RabbitMqClient")


class RabbitMQClient:

    def __init__(self):
        self.username = config.rabbit_username
        self.password = config.rabbit_password
        self.host = config.rabbit_host
        self.port = config.rabbit_port
        self.queue = config.rabbit_queue
        self.dl_queue = config.rabbit_dlqueue
        self.exchange = config.rabbit_exchange
        self.routing_key = config.rabbit_routing_key
        self.dl_routing_key = config.rabbit_dl_routing_key
        self.vhost = config.rabbit_vhost
        self.type = 'application/json'

    def bind_queue_to_exchange(self, channel, queue=config.rabbit_queue,
                               rk=config.rabbit_routing_key):
        """
        channel - Can be extracted from the connection
        queue   - Once a queue is declared
        """

        try:
            channel.queue_bind(queue=queue, exchange=self.exchange,
                               routing_key=rk)
        except Exception as e:
            mq_logger.error(e)
            mq_logger.error("Unable to bind queue:{0} to exchange:{1} with RK: {2}".format(
                queue, (self.exchange), rk))
            exit(1)

        mq_logger.info("Successfully bound queue: {0} to exchange: {1} with RK: {2}".format(
            queue, (self.exchange), rk))
        return

    def consume(self, callback):
        connection = self.connect_to_mq()
        channel = connection.channel()

        # Create the Dedicated Rabbit Queue
        self.declare_queue(channel)
        self.bind_queue_to_exchange(channel)

        # Create the DLQ
        self.declare_queue(channel, queue_name=self.dl_queue)
        self.bind_queue_to_exchange(channel, queue=self.dl_queue,
                                    rk=config.rabbit_dl_routing_key)

        # Basic consume reads the message off the queue with
        # ch, method, properties, body as the params
        channel.basic_consume(callback,
                              queue=self.queue,
                              no_ack=True)

        mq_logger.info('Waiting for messages from queue: {}'.format
                       (self.queue))

        channel.start_consuming()

    def connect_to_mq(self):
        mq_logger.debug('Connecting to mq...')
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host, int(self.port), self.vhost, credentials, ssl=False)

        try:
            connection = pika.BlockingConnection(parameters)
            mq_logger.info('Successfully connected to rabbit!')
        except Exception as e:
            mq_logger.error(e)
            exit(1)

        return connection

    def dead_letter_tweet(self, tweets):
        mq_logger.error("Dead lettering tweet '{}'".format(tweets))
        self.publish_to_mq(tweets, rk=self.dl_routing_key)

    def declare_queue(self, channel, queue_name=config.rabbit_queue):
        """
        If the queue doesn't exists create it and
        bind to to an exchange
        """
        try:
            channel.queue_declare(queue=queue_name)
        except Exception as e:
            mq_logger.error(e)
            mq_logger.error("Unable to declare queue:{}".format(queue_name))
            exit(1)
        mq_logger.info("Successfully declared queue: {}".format(queue_name))

    def publish_to_mq(self, tweets, rk=config.rabbit_routing_key):
        """
        @tweets - An Array of one or many tweets as json, see Tweet.to_tweet()
        """
        channel = self.connect_to_mq().channel()
        mq_logger.info(
            'Attempting to publish {} tweet(s) to rabbit.'.format(len(tweets)))
        for tweet in tweets:

            try:
                channel.basic_publish(self.exchange,
                                      rk,
                                      tweet,
                                      pika.BasicProperties(content_type=self.type,
                                                           delivery_mode=1))
                mq_logger.info(
                    "Published Message: {0} to exchange: {1} with key: {2}"
                    .format(tweet, (self.exchange), rk))

            except Exception as e:
                mq_logger.error(e)
                raise

        channel.close()
