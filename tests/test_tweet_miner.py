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

    
