import logging


class FailurePostToAPI(Exception):
    def __init__(self, status_code, content=None):

        if content is not None:
            self.msg = "FPTA:{0}:Content:{1}".format(status_code, content)
        else:
            self.msg = "Failed To Post Converted Tweet To API. HTTPStatus Code:{}".format(
                status_code)

    def __str__(self):
        return "{}".format(self.msg)


class MissingPayloadException(Exception):
    def __init__(self, tweet):
        self.msg = "Tweet '{}' is missing payload.".format(tweet)

    def __str__(self):
        return "{}".format(self.msg)


class InvalidPayloadException(Exception):
    def __init__(self, payload):
        self.msg = "Payload '{}' Is Invalid. Cannot mine accurately".format(
            payload)

    def __str__(self):
        return "{}".format(self.msg)


class DatetimeException(Exception):
    def __init__(self, created_at):
        self.msg = "Can't extract datetime from created_at: {}".format(
            created_at)

    def __str__(self):
        return "{}".format(self.msg)
