from lib.rabbitmq_client import RabbitMQClient
from lib.tweet_miner import TweetMiner
from time import sleep
import queue
from json import loads
from multiprocessing import Process
from lib.exceptions import MissingPayloadException, InvalidPayloadException
import logging
from lib.logger import Logger
from json import dumps
Logger.initiate_logger()
main_logger = logging.getLogger("Main")
mq = RabbitMQClient()


# Called when a message arrives onto the queue
def callback(ch, method, properties, body):
    # mq_logger.debug
    main_logger.info('Picked up: {}'.format(str(body)))

    try:
        tweet = loads(body)
    except Exception:
        main_logger.error("Unable to convert {} into json".format(body))
        return

    try:
        tm = TweetMiner(tweet)
        event = tm.return_event_from_tweet()
    except (MissingPayloadException, InvalidPayloadException) as e:
        main_logger.error(e)
        mq.dead_letter_tweet([tweet])
        return

    main_logger.info("Successfully mined tweet into Event: {}".format(
        dumps(event, indent=4, sort_keys=True)))


def main():

    mq.consume(callback)


main()
