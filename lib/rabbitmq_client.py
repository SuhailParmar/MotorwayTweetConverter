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
        self.source_queue = config.rabbit_source_queue
        self.dl_queue = config.rabbit_dlqueue
        self.exchange = config.rabbit_exchange
        self.routing_key = config.rabbit_routing_key
        self.dl_routing_key = config.rabbit_dl_routing_key
        self.vhost = config.rabbit_vhost
        self.type = 'application/json'

    def consume(self, callback):
        connection = self.connect_to_mq()
        channel = connection.channel()

        # Basic consume reads the message off the queue with
        # ch, method, properties, body as the params
        channel.basic_consume(callback,
                              queue=self.source_queue,
                              no_ack=True)

        mq_logger.info('Waiting for messages from queue: {}'.format
                       (self.source_queue))

        try:
            channel.start_consuming()
        except (Exception, KeyboardInterrupt) as e:
            mq_logger.error(e)
            mq_logger.error('Closing Connection.')
            channel.close()
            return

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

    def dead_letter_tweet(self, tweet, reason):
        tweet = dumps(tweet)  # Convert to string
        mq_logger.warn("Dead lettering tweet '{}'".format(tweet))

        channel = self.connect_to_mq().channel()

        mq_logger.debug(
            'Attempting to publish event {} to rabbit.'.format(tweet))

        props = pika.BasicProperties(content_type=self.type,
                                     headers={"reason": reason.msg},
                                     delivery_mode=1)
        try:
            channel.basic_publish(self.exchange,
                                  self.dl_routing_key,
                                  tweet,
                                  props
                                  )
            mq_logger.info(
                "Dead Lettered Event: {0} to exchange: {1} with key: {2}"
                .format(tweet, (self.exchange), self.dl_routing_key))
        except Exception as e:
            mq_logger.error(e)
            raise
        channel.close()
