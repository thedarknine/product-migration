"""Provides all methods to interact with Plane."""

import os
from dotenv import load_dotenv
from sources.models.plane import Project as PlProject, User as PlUser, Task as PlTask
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

    def get_total(self, elements_list: dict) -> int:
        """Retrieve the total number of elements from Plane.

        Returns:
            int: The total number of elements.
        """
        logs.get_logger().info("Attempting to get total number from Plane")
        return elements_list["total_count"]

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

    def get_all_tasks_by_project(self, project_id: str) -> list:
        """Get all tasks from Plane by project.

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
                os.getenv("PLANE_PATH_TASKS"),
                "{PROJECT_ID}",
                project_id,
                # params="&per_page=" + str(super().get_default_size())
                # + "&cursor=" cursor doesn't work
                # + str(loop),
            )
            if tasks_result is None:
                break
            tmp_tasks_list = self.compute_tasks(tasks_result)
            total = (
                self.get_total(tasks_result)
                if "total_count" in tasks_result
                else int(super().get_default_size())
            )
            remaining = total - (loop * int(super().get_default_size()))
            tasks_list = list(
                set(
                    tasks_list
                    + [PlTask.model_validate(task) for task in tmp_tasks_list]
                )
            )
            loop += 1
        return tasks_list

    def compute_tasks(self, tasks_list: dict, exclude_tasks: list = None) -> list:
        """Retrieve a list of tasks from Plane.

        Args:
            tasks_list (dict): A list of tasks.
            exclude_tasks (list): A list of tasks to exclude by name.

        Returns:
            list: A list of tasks.
        """
        logs.get_logger().info("Compute tasks from Plane")
        exclude_tasks = [] if exclude_tasks is None else exclude_tasks
        return [
            task for task in tasks_list["results"] if task["name"] not in exclude_tasks
        ]
