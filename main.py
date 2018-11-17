from lib.rabbitmq_client import RabbitMQClient
from lib.tweet_miner import TweetMiner
from lib.exceptions import MissingPayloadException
from lib.exceptions import InvalidPayloadException
from lib.exceptions import FailurePostToAPI
from lib.logger import Logger
from lib.requests import Requests
from json import loads
import logging

Logger.initiate_logger()
main_logger = logging.getLogger("Main")
mq = RabbitMQClient()
req = Requests()


# Called when a message arrives onto the queue
def callback(ch, method, properties, body):
    main_logger.debug('Picked up: {}'.format(str(body)))

    try:
        # Convert to a python json object first for easy parsing
        tweet = loads(body)
    except Exception:
        main_logger.error("Unable to convert {} into json".format(body))
        mq.dead_letter_tweet({"invalid_json": str(body)},
                             'Failure converting body to json')
        return

    try:
        # Attempt to mine the tweet
        tm = TweetMiner(tweet)
        event = tm.return_event_from_tweet()
        req.post_to_api(event)

    except (MissingPayloadException, InvalidPayloadException,
            FailurePostToAPI) as e:
        # Dead letter the event
        main_logger.error(e)
        mq.dead_letter_tweet(tweet, e)


def main():
    mq.consume(callback)


main()
