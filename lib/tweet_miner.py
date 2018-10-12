from re import compile
from time import strptime, mktime
from datetime import datetime


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
        pattern = compile("[M][0-9]{1,2}")
        motorway = pattern.search(value)

        if not motorway:
            print('Couldnt extract motorway from {0}:{1}'.format(
                tweet_field, value))
            raise LookupError

        motorway = motorway.group(0)
        motorway_number = motorway.replace("M", "", 1)
        return motorway_number

    def convert_datetime_to_timeblock(self):
        """
        Typical twitter_datetime = (Wed Oct 10 19:13:35 +0000 2018)
        """
        tweet_datetime = self.tweet["created_at"]
        # Lazy check correct format
        if len(tweet_datetime.split(" ")) != 6:
            print('Couldnt extract datetime from {}'.format(
                tweet_datetime))
            raise ValueError

        time_block = {}
        time_block["day_worded"] = tweet_datetime.split(" ")[0]
        # Convert into python datetime to easily extract minutes, hour etc
        time_pattern = strptime(tweet_datetime, "%a %b %d %H:%M:%S +0000 %Y")
        dt = datetime.fromtimestamp(mktime(time_pattern))

        time_block["timestamp"] = dt.isoformat()
        time_block["day_numerical"] = dt.day
        time_block["year"] = dt.year
        time_block["hour"] = dt.hour
        time_block["minutes"] = dt.minute
        time_block["seconds"] = dt.second

        return time_block


class Event:
    # The mined tweet output
    def __init__(self):
        self.event = {
            "motorway": -1,
            "id": -1,
            # Time block
            "timestamp": "",
            "day_numerical": -1,
            "day_worded": "",
            "year": -1,
            "hour": -1,
            "minutes": -1,
            "seconds": -1,
            # Data block
            "data": {
                "junction": -1,
                "direction": "",  # N,E,S,W
                "closest_city": "",
                "reason": "",
                "link": ""
            }
        }
