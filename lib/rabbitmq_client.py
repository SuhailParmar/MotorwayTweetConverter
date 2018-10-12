import pika
import logging
from json import dumps, loads
from sys import exit
import config as config

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

    def bind_to_mq(self):
        connection = self.connect_to_mq()
        mq_logger.info('Bound to queue: {}. Waiting for messages.'.format
                       (self.queue))

        channel = connection.channel()
        result = channel.queue_declare(queue=self.queue)
        queue = result.method.queue

        channel.basic_consume(self.callback,
                              queue=queue,
                              no_ack=True)

        channel.start_consuming()

    @staticmethod
    def callback(ch, method, properties, body):
        # mq_logger.debug('Picked up: {}'.format(body))
        print('Picked up: {}'.format(body))


if __name__ == "__main__":
    r = RabbitMQClient()
    r.bind_to_mq()
