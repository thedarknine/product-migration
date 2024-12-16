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

    def get_total(self, elements_list: dict) -> int:
        """Retrieve the total number of elements from OpenProject.

        Returns:
            int: The total number of elements.
        """
        logs.get_logger().info("Attempting to get total number from OpenProject")
        return elements_list["total"]

    def get_all_projects(self, exclude_projects: list = None) -> list:
        """Get all projects from OpenProject.

        Returns:
            list
                A list of projects.
        """
        projects_result = super().get_all(
            os.getenv("OPENPROJECT_PATH_PROJECTS"),
            params="&pageSize=" + str(super().get_default_size()),
        )
        projects_list = self.compute_projects(projects_result, exclude_projects)
        return [OPProject.model_validate(project) for project in projects_list]

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

    def get_all_users(self, exclude_users: list = None) -> list:
        """Get all users from OpenProject.

        Returns:
            list
                A list of users.
        """
        # Retrieve all users with pagination
        remaining = loop = 1
        users_list = []
        while remaining >= 0:
            users_result = super().get_all(
                os.getenv("OPENPROJECT_PATH_USERS"),
                params="&pageSize="
                + str(super().get_default_size())
                + "&offset="
                + str(loop),
            )
            tmp_users_list = self.compute_users(users_result, exclude_users)
            remaining = self.get_total(users_result) - (
                loop * int(super().get_default_size())
            )
            users_list = list(
                set(
                    users_list
                    + [OPUser.model_validate(user) for user in tmp_users_list]
                )
            )
            loop += 1
        return users_list

    def compute_users(self, users_list: dict, exclude_users: list = None) -> list:
        """Retrieve a list of users from OpenProject.

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
