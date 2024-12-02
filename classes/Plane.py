import logging
import os
import pprint
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
        return None
    
    def get_users(self):
        logging.info(f"Attempting to get users from Plane")
        users_list = []
        # First, get projects
        projects_list = self.get_projects()
        for project in projects_list or []:
            self.set_endpoint(str.replace(os.getenv("PLANE_PATH_USERS"), "{PROJECT_ID}", project["id"]))
            members_list = super().get()
            users_list.append([user for user in members_list if members_list])
        return users_list
