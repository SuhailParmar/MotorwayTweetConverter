from pytest import raises
from lib.tweet_miner import TweetMiner


class TestTweetMiner:
    # TODO Change from assignment to a[a] = b
    tm = TweetMiner({"screen_name": "Traffic_M6",
                     "created_at": "Wed Oct 10 19:13:35 +0000 2018",
                     "payload": ("#M6 J2 southbound exit (Coventry) -" +
                                 "Broken down vehicle - Full details at https:/" +
                                 "/t.co/nkWL91Ro1g (Updated every 5 minutes)")})

    def test_motorway_from_screen_name(self):
        assert self.tm.get_motorway_number() == "6"

    def test_motorway_hidden_in_screen_name(self):
        self.tm.tweet["screen_name"] = "TrafficM5asasaas"
        assert self.tm.get_motorway_number() == "5"

    def test_lookup_error_in_screen_name(self):
        self.tm.tweet["screen_name"] = "SuhailParmar"
        with(raises(LookupError)):
            assert self.tm.get_motorway_number()

    def test_convert_datetime_to_timeblock(self):
        self.tm.tweet["created_at"] = "Wed Oct 10 19:13:35 +0000 2018"
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

        self.tm.tweet["created_at"] = "Thu Apr 06 15:24:15 +0000 2017"
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

    def test_get_reported_junction(self):
        self.tm.tweet["payload"] =\
            "#M6 J2 southbound exit (Coventry) - Broken down vehicle - Full details at https://t.co/nkWL91Ro1g (Updated every 5 minutes)"

        assert self.tm.get_reported_junction() == ["J2"]

    def test_get_reported_junctions(self):
        self.tm.tweet["payload"] =\
            "#M6 northbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall) - Congestion - Full details at https://www.MotorwayCameras.co.uk/Traffic#M6  (Updated every 5 minutes)"

        assert self.tm.get_reported_junction() == ["J6", "J7"]

    def test_get_not_junction(self):
        self.tm.tweet["payload"] =\
            "#M6 northbound between (Birmingham) and (Birmingham (N) / Walsall) - Congestion - Full details at https://www.MotorwayCameras.co.uk/Traffic#M6  (Updated every 5 minutes)"

        with raises(LookupError):
            assert self.tm.get_reported_junction()

    def test_get_direction_of_incident(self):

        self.tm.tweet["payload"] =\
            "#M6 northbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall) - Congestion - Full details at https://www.MotorwayCameras.co.uk/Traffic#M6  (Updated every 5 minutes)"

        assert self.tm.get_direction_of_incident() == "n"

        self.tm.tweet["payload"] =\
            "#M6 eastbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall) - Congestion - Full details at https://www.MotorwayCameras.co.uk/Traffic#M6  (Updated every 5 minutes)"

        assert self.tm.get_direction_of_incident() == "e"

        self.tm.tweet["payload"] =\
            "#M6 southbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall) - Congestion - Full details at https://www.MotorwayCameras.co.uk/Traffic#M6  (Updated every 5 minutes)"

        assert self.tm.get_direction_of_incident() == "s"

        self.tm.tweet["payload"] =\
            "#M6 westbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall) - Congestion - Full details at https://www.MotorwayCameras.co.uk/Traffic#M6  (Updated every 5 minutes)"

        assert self.tm.get_direction_of_incident() == "w"

    def test_get_closest_city(self):

        self.tm.tweet["payload"] =\
            "#M6 westbound J6 (Birmingham) - Congestion - Full details at https://www.MotorwayCameras.co.uk/Traffic#M6  (Updated every 5 minutes)"

        assert self.tm.get_closest_city() == ["Birmingham"]

    def test_get_closest_cities(self):

        self.tm.tweet["payload"] =\
            "#M6 westbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall) - Congestion - Full details at https://www.MotorwayCameras.co.uk/Traffic#M6  (Updated every 5 minutes)"

        assert self.tm.get_closest_city() ==\
            ["Birmingham", "Birmingham (N) / Walsall"]
