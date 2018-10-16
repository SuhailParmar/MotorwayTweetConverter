from lib.rabbitmq_client import RabbitMQClient
from lib.tweet_miner import TweetMiner
from lib.threads import ConsumerThread, INBOUND_MSG_QUEUE
from time import sleep
import queue
from json import loads
from multiprocessing import Process


def callback(ch, method, properties, body):
    # mq_logger.debug
    print('Picked up: {}'.format(str(body)))
    tweet = loads(body)

    tm = TweetMiner(tweet)
    event = tm.return_event_from_tweet()
    print("{}".format(event))


def main():

    mq = RabbitMQClient()
    channel = mq.connect_to_mq().channel()

    mq.declare_queue(channel)
    mq.bind_queue_to_exchange(channel)

    # Basic consume reads the message off the queue with
    # ch, method, properties, body as the params
    channel.basic_consume(callback,
                          queue=mq.queue,
                          no_ack=True)

    print('Bound to queue: {}. Waiting for messages.'.format
          (mq.queue))

    channel.start_consuming()


main()
