"""
Provides generic methods to interact with APIs
"""
import urllib.parse
import httpx
from dotenv import load_dotenv
from utilities import logs

load_dotenv()

class Client:
    """ Client class to interact with APIs """

    def __init__(self, base_url, path=None, headers=None):
        self.base_url = base_url
        self.path = path or ''
        self.headers = headers or {}
        self.__endpoint = None

    def get_endpoint(self):
        """ Endpoint attribute getter """
        return self.__endpoint

    def set_endpoint(self, path):
        """ Endpoint attribute gsetter """
        if len(path) != 0:
            self.__endpoint = urllib.parse.urljoin(self.base_url, path)

    def get(self, params=None):
        """ Get method for API calls """
        logger = logs.get_logger()
        try:
            logger.info(f"Attempting to get list from: {self.get_endpoint()}")
            with httpx.Client() as client:
                response = client.get(self.get_endpoint(), headers=self.headers, params=params)
                #print(response.url)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error("An error occurred: {e}")
            print(f"An error occurred: {e}")
            return None
