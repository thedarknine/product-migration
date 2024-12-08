"""
Provides all methods to interact with OpenProject
"""
import os
from dotenv import load_dotenv
from classes import api as Api
from utilities import logs

load_dotenv()

class Client(Api.Client):
    """ Client class to interact with OpenProject """

    def __init__(self):
        headers = { 'Authorization': os.getenv("OPENPROJECT_API_AUTH") }
        super().__init__(os.getenv("OPENPROJECT_URL"), headers=headers)

    def get_projects(self):
        """
        Retrieves a list of projects from OpenProject.

        Returns:
            list: A list of projects.
        """
        logs.get_logger().info("Attempting to get projects from OpenProject")
        self.set_endpoint(os.getenv("OPENPROJECT_PATH_PROJECTS"))
        excluded_projects = os.getenv("OPENPROJECT_EXCLUDED_PROJECTS", "").split(',')
        projects_list = super().get()["_embedded"]["elements"]
        return [project for project in projects_list
                if project["name"] not in excluded_projects]

    def get_users(self):
        """
        Retrieves a list of users from Plane.

        Returns:
            list: A list of users.
        """
        logs.get_logger().info("Attempting to get users from OpenProject")
        self.set_endpoint(os.getenv("OPENPROJECT_PATH_USERS"))
        return super().get()["_embedded"]["elements"]

    # Closed tickets : [{ "status_id": { "operator": "c" }}]
    # Open tickets : [{ "status_id": { "operator": "o" }}]
    def get_tasks(self):
        """
        Retrieves a list of tasks from Plane.

        Returns:
            list: A list of tasks.
        """
        logs.get_logger().info("Attempting to get tasks from OpenProject")
        # First, get projects
        projects_list = self.get_projects()
        all_tasks = []
        for project in projects_list or []:
            self.set_endpoint(str.replace(os.getenv("OPENPROJECT_PATH_TASKS"),
                                          "{PROJECT_ID}", str(project["id"])))
            # Retrieve paginated results
            remaining = loop = 1
            while remaining >= 0:
                tasks_list = super().get('[{"status_id":{"operator":"o"}}]&offset='
                                         + str(loop) + '&pageSize=10')
                all_tasks.extend([task for task in tasks_list["_embedded"]["elements"]
                                  if tasks_list])
                remaining = tasks_list["total"] - (tasks_list["offset"] * 10)
                loop += 1
        return all_tasks
