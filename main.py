from lib.rabbitmq_client import RabbitMQClient
from lib.tweet_miner import TweetMiner
from time import sleep
import queue
from json import loads
from multiprocessing import Process
from lib.exceptions import *

# Called when a message arrives onto the queue


def callback(ch, method, properties, body):
    # mq_logger.debug
    print('Picked up: {}'.format(str(body)))

    try:
        tweet = loads(body)
    except Exception:
        print("Unable to convert {} into json".format(body))
        return

    try:
        tm = TweetMiner(tweet)
    except (MissingPayloadException, InvalidPayloadException) as e:
        print(e)
        return

    event = tm.return_event_from_tweet()
    print("{}".format(event))


def main():

    mq = RabbitMQClient()
    mq.consume(callback)


main()
