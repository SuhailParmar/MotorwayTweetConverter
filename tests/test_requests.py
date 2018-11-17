from lib.requests import Requests
from lib.exceptions import FailurePostToAPI
import requests_mock
from pytest import raises


class TestRequests():
    """
    Testing the interactions with the MotorwayAPI
    """

    r = Requests()

    def test_raises_error_on_post_if_api_is_down(self):
        with requests_mock.Mocker() as mock:
            mock.post('http://localhost:8000/api/events', status_code=404)

            with raises(FailurePostToAPI):
                assert self.r.post_to_api('bum')
