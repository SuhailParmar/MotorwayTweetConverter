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

    def test_converts_datetime_to_isoformat(self):
        self.tm.tweet = {"created_at": "Wed Oct 10 19:13:35 +0000 2018"}
        assert self.tm.convert_datetime_to_isoformat() == "2018-10-10T19:13:35"
        self.tm.tweet = {"created_at": "Mon May 11 16:02:30 +0000 1997"}
        assert self.tm.convert_datetime_to_isoformat() == "1997-05-11T16:02:30"
