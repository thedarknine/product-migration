import logging
import os
import requests
from utilities import api

plane_url = os.getenv("PLANE_URL")
plane_headers = {
    'X-API-Key': os.getenv("PLANE_API_KEY")
}

def get_projects():
    try:
        logging.info(f"Attempting to get users from Plane")
        project_names_list = []
        projects_list = api.get_all(plane_url, os.getenv("PLANE_PATH_PROJECTS"), plane_headers)
        if projects_list:
            for project in projects_list["results"]:
                project_names_list.append(project["name"]) if project["name"] not in project_names_list else project_names_list
        return project_names_list
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return None

def get_users():
    try:
        logging.info(f"Attempting to get users from Plane")
        users_list = []
        projects_list = api.get_all(plane_url, os.getenv("PLANE_PATH_PROJECTS"), plane_headers)
        if projects_list:
            for project in projects_list["results"]:
                members_list = api.get_all(plane_url, str.replace(os.getenv("PLANE_PATH_USERS"), "{PROJECT_ID}", project["id"]), plane_headers)
                if members_list:
                    for user in members_list:
                        users_list.append(user["email"]) if user["email"] not in users_list else users_list
        return users_list
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return None