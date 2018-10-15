from pytest import raises
from lib.tweet_miner import TweetMiner


class TestTweetMiner:
    """
    For the purpose of these tests we will be assigning values directly
    to the self.payload_ attributes. To save computation splitting the
    string into an array for each test.
    """
    tm = TweetMiner({"screen_name": "Traffic_M6",
                     "id": 1,
                     "created_at": "Wed Oct 10 19:13:35 +0000 2018",
                     "payload": ("#M6 J2 southbound exit (Coventry) - Broken down vehicle - Full details at https://t.co/nkWL91Ro1g (Updated every 5 minutes)")})

    def test_splitting_payload(self):
        # __split__ is called in the constructor
        assert self.tm.payload_location == "#M6 J2 southbound exit (Coventry)"
        assert self.tm.payload_reason == "Broken down vehicle"
        assert self.tm.payload_further_info ==\
            "Full details at https://t.co/nkWL91Ro1g (Updated every 5 minutes)"

    def test_motorway_from_screen_name(self):
        assert self.tm.get_motorway_number() == 6

    def test_motorway_hidden_in_screen_name(self):
        self.tm.tweet["screen_name"] = "TrafficM6asasaas"
        assert self.tm.get_motorway_number() == 6

    def test_lookup_error_in_screen_name(self):
        self.tm.tweet["screen_name"] = "SuhailParmar"
        with(raises(LookupError)):
            assert self.tm.get_motorway_number()

    def test_convert_datetime_to_timeblock(self):
        self.tm.tweet["created_at"] = "Wed Oct 10 19:13:35 +0000 2018"
        time_block = self.tm.convert_datetime_to_timeblock()

        assert time_block["time_timestamp"] == '2018-10-10T19:13:35'
        assert time_block["time_day_numerical"] == 10
        assert time_block["time_day_worded"] == "Wed"
        assert time_block["time_year"] == 2018
        assert time_block["time_hour"] == 19
        assert time_block["time_minutes"] == 13
        assert time_block["time_seconds"] == 35

        self.tm.tweet["created_at"] = "Thu Apr 06 15:24:15 +0000 2017"
        time_block = self.tm.convert_datetime_to_timeblock()

        assert time_block["time_timestamp"] == '2017-04-06T15:24:15'
        assert time_block["time_day_numerical"] == 6
        assert time_block["time_day_worded"] == "Thu"
        assert time_block["time_year"] == 2017
        assert time_block["time_hour"] == 15
        assert time_block["time_minutes"] == 24
        assert time_block["time_seconds"] == 15

    def test_get_reported_junction(self):
        self.tm.payload_location = "#M6 J2 southbound exit (Coventry)"
        assert self.tm.get_reported_junction() == [2]

    def test_get_reported_junctions(self):
        self.tm.payload_location =\
            "#M6 northbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall)"

        assert self.tm.get_reported_junction() == [6, 7]

    def test_get_not_junction(self):
        self.tm.payload_location =\
            "#M6 northbound between (Birmingham) and (Birmingham (N) / Walsall)"

        with raises(LookupError):
            assert self.tm.get_reported_junction()

    def test_get_direction_of_incident_north(self):

        self.tm.payload_location = "#M6 northbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall)"
        assert self.tm.get_direction_of_incident() == "n"

    def test_get_direction_of_incident_east(self):

        self.tm.payload_location = "#M6 eastbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall)"
        assert self.tm.get_direction_of_incident() == "e"

    def test_get_direction_of_incident_south(self):

        self.tm.payload_location =\
            "#M6 southbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall)"

        assert self.tm.get_direction_of_incident() == "s"

    def test_get_direction_of_incident_west(self):

        self.tm.payload_location =\
            "#M6 westbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall)"

        assert self.tm.get_direction_of_incident() == "w"

    def test_get_nearest_city(self):

        self.tm.payload_location = "#M6 westbound J6 (Birmingham)"

        assert self.tm.get_nearest_cities() == ["Birmingham"]

    def test_ge_nearest_cities(self):

        self.tm.payload_location =\
            "#M6 westbound between J6 (Birmingham) and J7 (Birmingham (N) / Walsall)"

        assert self.tm.get_nearest_cities() ==\
            ["Birmingham", "Birmingham (N) / Walsall"]

    def test_get_incident(self):
        self.tm.payload_reason = "Broken down vehicle"
        assert self.tm.get_reason_for_incident() == "broken down vehicle"

    def test_returned_event_from_tweet(self):
        self.tm =\
            TweetMiner({"screen_name": "Traffic_M6",
                        "id": 1,
                        "created_at": "Wed Oct 10 19:13:35 +0000 2018",
                        "payload": ("#M6 J2 southbound exit (Coventry) - Broken down vehicle - Full details at https://t.co/nkWL91Ro1g (Updated every 5 minutes)")})

        event = self.tm.return_event_from_tweet()
        assert event["motorway"] == 6
        assert event["id"] == 1
        assert event["junction"] == [2]
        assert event["direction"] == 's'
        assert event["closest_cities"] == ["Coventry"]
        assert event["reason"] == "broken down vehicle"

        assert event["time_timestamp"] == "2018-10-10T19:13:35"
        assert event["time_day_numerical"] == 10
        assert event["time_day_worded"] == "Wed"
        assert event["time_year"] == 2018
        assert event["time_hour"] == 19
        assert event["time_minutes"] == 13
        assert event["time_seconds"] == 35
