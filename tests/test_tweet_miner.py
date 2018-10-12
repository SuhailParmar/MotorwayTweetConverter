from lib.tweet_miner import TweetMiner
from pytest import raises


class TestTweetMiner:

    tm = TweetMiner({"screen_name": "Traffic_M6"})

    def test_motorway_from_screen_name(self):
        assert self.tm.get_motorway_number() == "6"

    def test_motorway_hidden_in_screen_name(self):
        self.tm.tweet = {"screen_name": "TrafficM6asasaas"}
        assert self.tm.get_motorway_number() == "6"

    def test_lookup_error_in_screen_name(self):
        self.tm.tweet = {"screen_name": "SuhailParmar"}
        with(raises(LookupError)):
            assert self.tm.get_motorway_number()

    def test_convert_datetime_to_timeblock(self):
        self.tm.tweet = {"created_at": "Wed Oct 10 19:13:35 +0000 2018"}
        assert self.tm.convert_datetime_to_timeblock() ==\
            {
            "timestamp": '2018-10-10T19:13:35',
            "day_numerical": 10,
            "day_worded": "Wed",
            "year": 2018,
            "hour": 19,
            "minutes": 13,
            "seconds": 35
        }

        self.tm.tweet = {"created_at": "Thu Apr 06 15:24:15 +0000 2017"}
        assert self.tm.convert_datetime_to_timeblock() ==\
            {
            "timestamp": '2017-04-06T15:24:15',
            "day_numerical": 6,
            "day_worded": "Thu",
            "year": 2017,
            "hour": 15,
            "minutes": 24,
            "seconds": 15
        }
