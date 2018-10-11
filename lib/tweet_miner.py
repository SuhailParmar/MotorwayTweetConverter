import re


class TweetMiner:
    """
    The aim of this class is to split the tweet into seperate
    data fields.
    """

    def __init__(self, tweet):
        self.tweet = tweet
        self.event = Event

    def get_motorway_number(self, tweet_field="screen_name"):
        """
        tweet_field = ["screen_name", payload"]
        Motorway number can be derived from the payload or screen_name
        """
        value = self.tweet[tweet_field]
        # Strip everything apart from a MX or MXX
        pattern = re.compile("[M][0-9]{1,2}")
        motorway = pattern.search(value)

        if not motorway:
            print('Couldnt extract motorway from {0}:{1}'.format(
                tweet_field, value))
            raise LookupError

        motorway = motorway.group(0)
        motorway_number = motorway.replace("M", "", 1)
        return motorway_number


class Event:
    # The mined tweet output
    def __init__(self):
        self.event = {
            "motorway": -1,
            "timestamp": "",
            "id": -1,
            "day_numerical": -1,
            "day_worded": "",
            "year": -1,
            "hour": -1,
            "minutes": -1,
            "seconds": -1,
            "miliseconds": -1,
            "data": {
                "junction": -1,
                "direction": "",  # N,E,S,W
                "closest_city": "",
                "reason": "",
                "link": ""
            }
        }
