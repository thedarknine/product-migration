import logging
import httpx
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

class Client:
    def __init__(self, base_url, path=None, headers=None):
        self.base_url = base_url
        self.path = path or ''
        self.headers = headers or {}
        self.__endpoint = None
    
    def get_endpoint(self):
        return self.__endpoint
    
    def set_endpoint(self, path):
        if len(path) != 0:
            self.__endpoint = urllib.parse.urljoin(self.base_url, path)
    
    def get(self):
        try:
            logging.info(f"Attempting to get list from: {self.get_endpoint()}")
            with httpx.Client() as client:
                response = client.get(self.get_endpoint(), headers=self.headers)
                response.raise_for_status() 
                return response.json()
        except httpx.HTTPError as e:
            logging.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")
            return None
