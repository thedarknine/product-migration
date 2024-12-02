import logging
import os
from dotenv import load_dotenv
from classes import Api

load_dotenv()

class Client(Api.Client):
    """ Client class to interact with Plane """
    
    def __init__(self):
        headers = { 'X-API-Key': os.getenv("PLANE_API_KEY") }
        super().__init__(os.getenv("PLANE_URL"), headers=headers)
        self.__endpoint = None

    def get_projects(self):
        logging.info(f"Attempting to get projects from Plane")
        self.set_endpoint(os.getenv("PLANE_PATH_PROJECTS"))
        if self.get_endpoint() != None:
            return super().get()["results"]