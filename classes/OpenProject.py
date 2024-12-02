import logging
import os
from dotenv import load_dotenv
from classes import Api

load_dotenv()

class Client(Api.Client):
    """ Client class to interact with OpenProject """
    
    def __init__(self):
        headers = { 'Authorization': os.getenv("OPENPROJECT_API_AUTH") }
        super().__init__(os.getenv("OPENPROJECT_URL"), headers=headers)
        self.__endpoint = None

    def get_projects(self):
        logging.info(f"Attempting to get projects from OpenProject")
        self.set_endpoint(os.getenv("OPENPROJECT_PATH_PROJECTS"))
        if self.get_endpoint() != None:
            excluded_projects = os.getenv("OPENPROJECT_EXCLUDED_PROJECTS", "").split(',')
            projects_list = super().get()["_embedded"]["elements"]
            return [project for project in projects_list if project["name"] not in excluded_projects ]
        return None
    
    # Tickets fermés : [{ "status_id": { "operator": "c" }}]
    # Tickets ouverts : [{ "status_id": { "operator": "o" }}]
    def get_tasks(self):
        logging.info(f"Attempting to get tasks from OpenProject")
        # First, get projects
        projects_list = self.get_projects()
        for project in projects_list or []:
            self.set_endpoint(str.replace(os.getenv("OPENPROJECT_PATH_TASKS"), "{PROJECT_ID}", str(project["id"])))
            print(self.get_endpoint())
            tasks_list = super().get('[{"status_id":{"operator":"o"}}]')["_embedded"]["elements"]
            print(len(tasks_list))


    # def get_project_names(self):
    #     logging.info(f"Attempting to get projects from OpenProject")
    #     self.set_endpoint(os.getenv("OPENPROJECT_PATH_PROJECTS"))
    #     if self.get_endpoint() != None:
    #         excluded_projects = os.getenv("OPENPROJECT_EXCLUDED_PROJECTS", "").split(',')
    #         project_names_list = []
    #         projects_list = super().get()["_embedded"]["elements"]
    #         for project in projects_list or []:
    #             if project["name"] not in excluded_projects:
    #                 project_names_list.append(project["name"]) if project["name"] not in project_names_list else project_names_list
    #         return project_names_list

    def get_users(self):
        logging.info(f"Attempting to get users from OpenProject")
        self.set_endpoint(os.getenv("OPENPROJECT_PATH_USERS"))
        if self.get_endpoint() != None:
            return super().get()["_embedded"]["elements"]