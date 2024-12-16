"""Provides all methods to interact with OpenProject."""

import os
from dotenv import load_dotenv
from sources.models.openproject import (
    Project as OPProject,
    User as OPUser,
    Task as OPTask,
)
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

    def get_all_tasks_by_project(self, project_id: str) -> list:
        """Get all tasks from OpenProject by project.

        Args:
            project_id (str): The project id.

        Returns:
            list
                A list of tasks.
        """
        # Retrieve all tasks with pagination
        remaining = loop = 1
        tasks_list = []
        while remaining >= 0:
            tasks_result = super().get_all(
                os.getenv("OPENPROJECT_PATH_TASKS"),
                "{PROJECT_ID}",
                project_id,
                params="&pageSize="
                + str(super().get_default_size())
                + "&offset="
                + str(loop),
            )
            if tasks_result is None:
                break
            tmp_tasks_list = self.compute_tasks(tasks_result)
            remaining = self.get_total(tasks_result) - (
                loop * int(super().get_default_size())
            )
            tasks_list = list(
                set(
                    tasks_list
                    + [OPTask.model_validate(task) for task in tmp_tasks_list]
                )
            )
            loop += 1
        return tasks_list

    def compute_tasks(self, tasks_list: dict) -> list:
        """Retrieve a list of tasks from OpenProject.

        Examples:
            - Closed tickets : [{ "status_id": { "operator": "c" }}]
            - Open tickets : [{ "status_id": { "operator": "o" }}]

        Returns:
            list: A list of tasks.
        """
        logs.get_logger().info("Compute tasks from OpenProject")
        return [
            task
            for task in tasks_list["_embedded"]["elements"]
            if task["subject"] not in tasks_list
        ]
