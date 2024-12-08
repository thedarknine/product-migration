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
        if not base_url:
            raise ValueError("base_url is required")
        self.base_url = base_url
        self.path = path or ''
        self.headers = headers or {}
        self.__endpoint = None

    def get_endpoint(self):
        """ Endpoint attribute getter """
        if self.__endpoint is None:
            self.set_endpoint(self.path)
        return self.__endpoint

    def set_endpoint(self, path):
        """ Endpoint attribute setter """
        if path and len(path) != 0:
            self.__endpoint = urllib.parse.urljoin(self.base_url, path)
        else:
            self.__endpoint = self.base_url

    def get(self, params=None):
        """ Get method for API calls """
        logger = logs.get_logger()
        try:
            logger.info("Attempting to get list from: %s", self.get_endpoint())
            with httpx.Client() as client:
                response = client.get(self.get_endpoint(), headers=self.headers, params=params)
                #print(response.url)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error("An error occurred: %s", e)
            print(f"An error occurred: {e}")
            return None
