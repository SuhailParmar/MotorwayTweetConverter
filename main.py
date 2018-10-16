from lib.rabbitmq_client import RabbitMQClient
from lib.tweet_miner import TweetMiner
from lib.threads import ConsumerThread, MiningThread, INBOUND_MSG_QUEUE
from time import sleep
import queue

MSG_QUEUE = queue.Queue(0)


def callback(ch, method, properties, body):
    # mq_logger.debug
    print('Picked up: {}'.format(str(body)))
    return MSG_QUEUE.put(body)


def main():

    threads = [
        ConsumerThread(queue=MSG_QUEUE),
        MiningThread(queue=MSG_QUEUE)
    ]

    threads[0].start()
    threads[1].run()


main()
