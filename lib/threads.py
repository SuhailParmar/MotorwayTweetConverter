import threading
import queue
from lib.rabbitmq_client import RabbitMQClient
from lib.tweet_miner import TweetMiner

INBOUND_MSG_QUEUE = queue.Queue(0)


class Thread (threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue


class ConsumerThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self, "ConsumerThread", queue)

    def run(self):
        try:
            mq = RabbitMQClient(internal_queue=self.queue)
            mq.consume_from_queue()
        except Exception as e:
            print(e)
            print("bye")
            SystemExit


class MiningThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self, "TweetMiningThread", queue)
        print("BOOM")

    def run(self):
        tweet = INBOUND_MSG_QUEUE.get()
        if tweet:
            print("Got Tweet")
            tm = TweetMiner(tweet)
            event = tm.return_event_from_tweet()
            return event
        else:
            print("No queue")
