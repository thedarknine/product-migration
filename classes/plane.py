"""
Provides all methods to interact with Plane
"""
import os
from dotenv import load_dotenv
from classes import api as Api
from utilities import logs

load_dotenv()

class Client(Api.Client):
    """ Client class to interact with Plane """

    def __init__(self):
        """Client Constructor"""
        headers = {'X-API-Key': os.getenv("PLANE_API_KEY")}
        super().__init__(os.getenv("PLANE_URL"), headers=headers)

    def get_projects(self) -> list:
        """
        Retrieves a list of projects from Plane.

        Returns:
            list: A list of projects.
        """
        logs.get_logger().info("Attempting to get projects from Plane")
        self.set_endpoint(os.getenv("PLANE_PATH_PROJECTS"))
        if self.get_endpoint() is not None:
            return super().get()["results"]
        return None

    def get_users(self) -> list:
        """
        Retrieves a list of users from Plane.

        This method first retrieves a list of projects, then for each project, 
        it retrieves the list of members.
        The members are then added to the list of users.

        Returns:
            list: A list of users.
        """
        logs.get_logger().info("Attempting to get users from Plane")
        users_list = []
        # First, get projects
        projects_list = self.get_projects()
        for project in projects_list or []:
            self.set_endpoint(str.replace(
                os.getenv("PLANE_PATH_USERS"), "{PROJECT_ID}", project["id"]))
            members_list = super().get()
            users_list.append([user for user in members_list if members_list])
        return users_list
