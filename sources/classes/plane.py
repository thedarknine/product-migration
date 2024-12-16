"""Provides all methods to interact with Plane."""

import os
from dotenv import load_dotenv
from sources.classes import api as Api
from sources.utilities import logs

load_dotenv()


class Client(Api.Client):
    """Client class to interact with Plane."""

    def __init__(self):
        """Client Constructor."""
        headers = {"X-API-Key": os.getenv("PLANE_API_KEY")}
        super().__init__(os.getenv("PLANE_URL"), headers=headers)

    def get_all_projects(self, exclude_projects: list = None) -> list:
        """Get all projects from Plane.

        Returns:
            list
                A list of projects.
        """
        projects_result = super().get_all(os.getenv("PLANE_PATH_PROJECTS"))
        projects_list = self.compute_projects(projects_result, exclude_projects)
        return [PlProject.model_validate(project) for project in projects_list]

    def compute_projects(
        self, projects_list: dict, exclude_projects: list = None
    ) -> list:
        """Retrieve a list of projects from Plane.

        Returns:
            list: A list of projects.
        """
        logs.get_logger().info("Compute projects from Plane")
        exclude_projects = [] if exclude_projects is None else exclude_projects
        return [
            project
            for project in projects_list["results"]
            if project["name"] not in exclude_projects
        ]

    def get_all_users_by_project(
        self, project_id: str, exclude_users: list = None
    ) -> list:
        """Get all users from Plane.

        Returns:
            list
                A list of users.
        """
        users_result = super().get_all(
            os.getenv("PLANE_PATH_USERS"), "{PROJECT_ID}", project_id
        )
        users_list = self.compute_users(users_result, exclude_users)
        return [PlUser.model_validate(user) for user in users_list]

    def compute_users(self, users_list: dict, exclude_users: list = None) -> list:
        """Retrieve a list of users from Plane.

        Args:
            users_list (dict): A list of users.
            exclude_users (list): A list of users to exclude by email.

        Returns:
            list: A list of users.
        """
        logs.get_logger().info("Compute users from Plane")
        exclude_users = [] if exclude_users is None else exclude_users
        computed_list = users_list["results"] if "results" in users_list else users_list
        return [user for user in computed_list if user["email"] not in exclude_users]
