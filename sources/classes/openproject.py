"""Provides all methods to interact with OpenProject."""

import os
from dotenv import load_dotenv
from sources.classes import api as Api
from sources.utilities import logs

load_dotenv()


class Client(Api.Client):
    """Client class to interact with OpenProject."""

    def __init__(self):
        """Client Constructor."""
        headers = {"Authorization": os.getenv("OPENPROJECT_API_AUTH")}
        super().__init__(os.getenv("OPENPROJECT_URL"), headers=headers)

    def compute_projects(
        self, projects_list: dict, exclude_projects: list = None
    ) -> list:
        """Retrieve a list of projects from OpenProject.

        Args:
            projects_list (dict): A list of projects.
            exclude_projects (list): A list of projects to exclude.

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
        """Retrieve a list of users from Plane.

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

    # Closed tickets : [{ "status_id": { "operator": "c" }}]
    # Open tickets : [{ "status_id": { "operator": "o" }}]
    def get_tasks_by_projectid(self, project_id: int) -> list:
        """Retrieve a list of tasks from Plane.

        Returns:
            list: A list of tasks.
        """
        logs.get_logger().info("Attempting to get tasks from OpenProject")
        all_tasks = []
        self.set_endpoint(
            str.replace(
                os.getenv("OPENPROJECT_PATH_TASKS"),
                "{PROJECT_ID}",
                str(project_id),
            )
        )
        # Retrieve paginated results
        remaining = loop = 1
        while remaining >= 0:
            tasks_list = super().get(
                'filter=[{"status_id":{"operator":"c"}}]&offset='
                + str(loop)
                + "&pageSize=10"
            )
            all_tasks.extend(
                [task for task in tasks_list["_embedded"]["elements"] if tasks_list]
            )
            if "offset" not in tasks_list:
                break
            remaining = tasks_list["total"] - (tasks_list["offset"] * 10)
            loop += 1
        return all_tasks
