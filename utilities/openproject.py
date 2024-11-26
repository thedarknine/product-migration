import logging
import os
import requests
from utilities import api
from dotenv import load_dotenv

openproject_url = os.getenv("OPENPROJECT_URL")
openproject_headers = {
    'Authorization': os.getenv("OPENPROJECT_API_AUTH")
}
load_dotenv(os.getenv("OPENPROJECT_EXCLUDE_PROJECTS"))
exclude_projects = os.getenv("OPENPROJECT_EXCLUDE_PROJECTS", "").split(',')

def get_projects():
    try:
        logging.info(f"Attempting to get projects from OpenProject")
        project_names_list = []
        projects_list = api.get_all(openproject_url, os.getenv("OPENPROJECT_PATH_PROJECTS"), openproject_headers)
        if projects_list:
            for project in projects_list["_embedded"]["elements"]:
                if project["name"] not in exclude_projects:
                        project_names_list.append(project["name"]) if project["name"] not in project_names_list else project_names_list
        return project_names_list
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return None
    
def get_users():
    try:
        logging.info(f"Attempting to get users from Plane")
        user_emails_list = []
        users_list = api.get_all(openproject_url, os.getenv("OPENPROJECT_PATH_USERS"), openproject_headers)
        if users_list:
            for user in users_list["_embedded"]["elements"]:
                user_emails_list.append(user["email"]) if user["email"] not in user_emails_list else user_emails_list
        return user_emails_list
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return None