from lib.config import api_base_url
from lib.config import api_post_endpoint
from lib.config import api_port
from lib.exceptions import FailurePostToAPI
from requests import post


class Requests():

    def __init__(self):
        self.base_url = api_base_url
        self.api_port = api_port
        self.post_endpoint = api_post_endpoint
        self.uri = 'http://' + self.base_url + ':' + str(self.api_port) + '/' + self.post_endpoint

    def post_to_api(self, data):
        response = post(self.uri, json=data)

        if response.status_code != 200:
            raise FailurePostToAPI(response.status_code)

        return response.status_code
