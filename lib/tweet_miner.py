from re import compile
from time import strptime, mktime
from datetime import datetime
from lib.utils import Utils


class TweetMiner:
    """
    The aim of this class is to split the tweet into seperate
    data fields.
    """

    def __init__(self, tweet):
        self.tweet = tweet  # {created_at: x, id: x, payload: x}
        self.event = Event

        """
        self.location = ""
        self.reason = ""
        self.further_info = ""
        self.__split__()
        """

    """
    def __split__(self):

        A typical Traffic_Mx tweet is split into 3 sections:
        "(Location) - (Reason) - (Link to further info)
        The location


        if "payload" in self.tweet:  # Prevent KeyError
            payload = self.tweet["payload"]
            arr = payload.split(" - ")
            self.location = arr[0]
            self.reason = arr[1]
            self.further_info = arr[2]
    """

    def get_direction_of_incident(self):
        """
        direction: (east/north/west/south)bound
        """
        value = self.tweet["payload"]
        pattern = compile("[a-z]{4,5}bound")
        direction = pattern.search(value)

        if not direction:
            print('Couldnt extract direction from payload:{}'.format(
                value))
            raise LookupError

        direction = direction.group(0)
        return direction[0]  # The first letter suffices (nesw)

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

    def get_reported_junction(self):
        payload = self.tweet["payload"]

        # Spaced to prevent splitting cities e.g. Stoke-On-Trent
        split_payload = payload.split(" - ")
        location = split_payload[0]

        # Strip everything apart from a JX or JXX
        pattern = compile("[J][0-9]{1,2}")
        junctions = pattern.findall(location)

        if len(junctions) < 1:
            print('Couldnt extract junction from payload: {}'.format(
                payload))
            raise LookupError

        return junctions

    def get_closest_city(self):
        payload = self.tweet["payload"]

        # Spaced to prevent splitting cities e.g. Stoke-On-Trent
        split_payload = payload.split(" - ")
        location = split_payload[0]

        nearest_cities = Utils.extract_contents_of_nested_brackets(location)

        if len(nearest_cities) < 1:
            print('Couldnt extract nearest_cities from payload: {}'.format(
                payload))
            raise LookupError

        return nearest_cities


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
                "junction": [],  # Could be multiple Junctions affected
                "direction": "",  # N,E,S,W
                "closest_cities": [],  # if multiple junctions there'll be multiple close cities
                "incident": "",
                "link": ""
            }
        }
