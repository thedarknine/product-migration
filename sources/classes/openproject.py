"""
Provides all methods to interact with OpenProject
"""

import os
from dotenv import load_dotenv
from sources.classes import api as Api
from sources.utilities import logs

load_dotenv()


class Client(Api.Client):
    """Client class to interact with OpenProject"""

    def __init__(self):
        """Client Constructor"""
        headers = {"Authorization": os.getenv("OPENPROJECT_API_AUTH")}
        super().__init__(os.getenv("OPENPROJECT_URL"), headers=headers)

    def compute_projects(
        self, projects_list: dict, exclude_projects: list = None
    ) -> list:
        """
        Retrieves a list of projects from OpenProject.

        Returns:
            list: A list of projects.
        """
        logs.get_logger().info("Compute projects from OpenProject")
        exclude_projects = [] if exclude_projects is None else exclude_projects
        return [
            project
            for project in projects_list["_embedded"]["elements"]
            if project["name"] not in exclude_projects
        ]

    def compute_users(self, users_list: dict, exclude_users: list = None) -> list:
        """
        Retrieves a list of users from Plane.

        Returns:
            list: A list of users.
        """
        logs.get_logger().info("Compute users from OpenProject")
        exclude_users = [] if exclude_users is None else exclude_users
        return [
            user
            for user in users_list["_embedded"]["elements"]
            if user["email"] not in exclude_users
        ]


