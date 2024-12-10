"""
Provides generic methods to interact with APIs
"""

import urllib.parse
import httpx
from dotenv import load_dotenv
from utilities import logs

load_dotenv()


class Client:
    """Client class to interact with APIs"""

    def __init__(self, base_url: str, path: str = None, headers: dict = None):
        """
        Client Constructor

        Args:
            base_url (str): Base URL of the API.
            path (str, optional): Path to append to the base URL. Defaults to None.
            headers (dict, optional): Headers to include in the request. Defaults to None.
        """
        if not base_url:
            raise ValueError("base_url is required")
        self.base_url = base_url
        self.path = path or ""
        self.headers = headers or {}
        self.__endpoint = None

    def get_endpoint(self) -> str:
        """Endpoint attribute getter"""
        if self.__endpoint is None:
            self.set_endpoint(self.path)
        return self.__endpoint

    def set_endpoint(self, path: str) -> None:
        """Endpoint attribute setter"""
        if path and len(path) != 0:
            self.__endpoint = urllib.parse.urljoin(self.base_url, path)
        else:
            self.__endpoint = self.base_url

    def get(self, params: dict = None) -> dict:
        """
        Get method for API calls

        Args:
            params (dict, optional): Parameters to include in the request.

        Returns:
            dict: JSON response from the API
        """
        logger = logs.get_logger()
        try:
            logger.info("Attempting to get list from: %s", self.get_endpoint())
            with httpx.Client() as client:
                response = client.get(
                    self.get_endpoint(), headers=self.headers, params=params
                )
                # print(response.url)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error("An error occurred: %s", e)
            print(f"An error occurred: {e}")
            return None
