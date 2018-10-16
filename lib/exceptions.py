
class MissingPayloadException(Exception):
    def __init__(self, tweet, msg=None):
        if not msg:
            print("Tweet '{}'does not have a payload.".format(tweet))


class InvalidPayloadException(Exception):
    def __init__(self, payload, msg=None):
        if not msg:
            print("Payload {} Is Invalid. Cannot mine accurately"
                  .format(payload))


class DatetimeException(Exception):
    def __init__(self, created_at, msg=None):
        if not msg:
            print("Can't extract datetime from created_at: {}"
                  .format(created_at))
