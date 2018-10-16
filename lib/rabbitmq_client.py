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
        self.exchange = config.rabbit_exchange
        self.routing_key = config.rabbit_routing_key
        self.vhost = config.rabbit_vhost
        self.type = 'application/json'

    def connect_to_mq(self):
        mq_logger.info('Connecting to mq...')
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host, int(self.port), self.vhost, credentials, ssl=False)

        try:
            connection = pika.BlockingConnection(parameters)
            mq_logger.info('Successfully connected to rabbit.')
        except Exception as e:
            mq_logger.error(e)
            exit(1)

        return connection

    def consume_from_queue(self, global_queue):
        # Read from a rabbit queue and place on an internal queue
        # global_queue = python.queue.queue -------^
        channel = self.connect_to_mq().channel()
        queue = self.declare_queue(channel)
        self.bind_queue_to_exchange(channel)

        # Basic consume reads the message off the queue with
        # ch, method, properties, body as the params
        # Partial is used as a workaround to place the body
        # of the message onto the global_queue
        channel.basic_consume(partial(self.callback, global_queue=global_queue),
                              queue=queue,
                              no_ack=True)

        mq_logger.info('Bound to queue: {}. Waiting for messages.'.format
                       (self.queue))

        channel.start_consuming()

    def declare_queue(self, channel, queue_name=config.rabbit_queue):
        """
        If the queue doesn't exists create it and
        bind to to an exchange
        """
        try:
            channel.queue_declare(queue=self.queue)
        except Exception as e:
            print(e)
            print("Unable to declare queue:{}".format(queue_name))
            exit(1)

    def bind_queue_to_exchange(self, channel):
        """
        channel - Can be extracted from the connection
        queue   - Once a queue is declared
        """

        try:
            channel.queue_bind(queue=self.queue, exchange=self.exchange,
                               routing_key=self.routing_key)
        except Exception as e:
            print(e)
            print("Unable to bind queue:{} to exchange:{1} with RK:{2}".format(
                self.queue, self.exchange, self.routing_key))
            exit(1)

        return

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
                    'Published Message:{0} to queue:{1}'.format(tweet, self.queue))

            except Exception as e:
                mq_logger.error(e)
                raise

        channel.close()

