from lib.config import api_base_url
from lib.config import api_post_endpoint
from lib.config import api_port, api_client_id, api_client_secret
from lib.exceptions import FailurePostToAPI
from json import loads
from requests import post
import logging

mq_logger = logging.getLogger("Requests")


class Requests():

    def __init__(self):
        self.host = api_base_url
        self.api_port = api_port
        self.base_url = 'http://' + self.host + \
            ':' + str(self.api_port) + '/'
        self.post_endpoint = api_post_endpoint
        self.client_id = api_client_id
        self.client_secret = api_client_secret

        self.uri = self.base_url + self.post_endpoint
        self.provider_uri = self.base_url + 'oauth2/token/'

    def get_auth_token(self):
        """
        Authenticate to unmocked API using test credentials
        to retrieve and OAuth token
        """
        url = self.provider_uri
        grant_type = "client_credentials"
        logging.debug('Authenticating against OAUTH2 provider...')
        request = post(url,  # Request Auth token
                       data="grant_type={0}&client_id={1}&client_secret={2}"
                       .format(grant_type, self.client_id, self.client_secret),
                       headers={'Content-Type': 'application/x-www-form-urlencoded'})

        if request.status_code != 200:
            raise ValueError

        logging.debug('Authentication successful.')
        content = loads(request.content)
        return content['access_token']

    def post_to_api(self, data):
        logging.info('Posting Event to API...')
        token = self.get_auth_token()

        response = post(self.uri, headers={
            'Content-Type': 'application/json',
            'Authorization': "Bearer {0}".format(token),
            },
            data=data)

        if response.status_code != 201:
            raise FailurePostToAPI(response.status_code,
                                   loads(response.content))

        logging.info('Successfully Posted event to the API!')
        return response.status_code
