import logging


class FailurePostToAPI(Exception):
    def __init__(self, status_code, msg=None):
        self.sc = status_code
        if not msg:
            self.msg = "Failed To Post To API. HTTPStatus Code:{}".format(
                status_code)
        logging.error(self.msg)

    def __str__(self):
        return "{}".format(self.msg)


class MissingPayloadException(Exception):
    def __init__(self, tweet, msg=None):
        if not msg:
            logging.error(
                "MissingPayloadException: Tweet '{}'does not have a valid payload.".format(tweet))


class InvalidPayloadException(Exception):
    def __init__(self, payload, msg=None):
        if not msg:
            logging.error("Payload '{}' Is Invalid. Cannot mine accurately"
                          .format(payload))


class DatetimeException(Exception):
    def __init__(self, created_at, msg=None):
        if not msg:
            logging.error("Can't extract datetime from created_at: {}"
                          .format(created_at))
