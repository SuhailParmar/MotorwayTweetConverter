import pika
import logging
import queue

from json import dumps, loads
from sys import exit

import lib.config as config

mq_logger = logging.getLogger("RabbitMqClient")


class RabbitMQClient:

    def __init__(self, internal_queue):
        self.username = config.rabbit_username
        self.password = config.rabbit_password
        self.host = config.rabbit_host
        self.port = config.rabbit_port
        self.queue = config.rabbit_queue
        self.exchange = config.rabbit_exchange
        self.routing_key = config.rabbit_routing_key
        self.vhost = config.rabbit_vhost
        self.type = 'application/json'
        self.internal_queue = internal_queue  # Global msg Q

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

    def consume_from_queue(self):

        queue, channel = self.declare_and_bind_queue()
        # Overridden the callback with our custom callback
        channel.basic_consume(lambda ch, method, properties, body:
                              self.callback(ch, method, properties,
                                            body, self.internal_queue),
                              queue=queue,
                              no_ack=True)

        mq_logger.info('Bound to queue: {}. Waiting for messages.'.format
                       (self.queue))

        channel.start_consuming()

    def declare_and_bind_queue(self, q=config.rabbit_queue):
        """
        If the queue doesn't exists create it and
        bind to to an exchange
        """
        cn = self.connect_to_mq()
        channel = cn.channel()
        result = channel.queue_declare(queue=self.queue)

        if result:
            print("Connected!")
        else:
            print("Unable to declare queue:{}".format(q))
            exit(1)

        bound = channel.queue_bind(queue=q, exchange=self.exchange,
                                   routing_key=self.routing_key)
        if bound:
            print("Bound!")
        else:
            print("Unable to bind queue:{} to exchange:{1} with RK:{2}".format(
                q, self.exchange, self.routing_key))
            exit(1)

        return result.method.queue, channel

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

    @staticmethod
    def callback(ch, method, properties, body, internal_queue):
        # mq_logger.debug
        print('Picked up: {}'.format(str(body)))
        return internal_queue.put(body)
