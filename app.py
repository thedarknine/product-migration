"""
Main file for migration
"""
import os
import sys
import pprint
from datetime import datetime
from dotenv import load_dotenv
from classes import plane as Plane, openproject as OpenProject
from utilities import display, logs

# Load env variables
try:
    load_dotenv(os.getenv("PROJECT_NAME"))
except FileNotFoundError:
    sys.exit(display.alert("Configuration could not be loaded (" + repr(Exception) + ")"))

display.clear_screen()

# Initialize logs
logs.init_file()

# Initialize script info
start_date = datetime.now()
display.start_info(start_date, 'Migration')

def sync_projects(openproject_projects, plane_projects):
    """Check if project name exist into new tool"""
    for project in openproject_projects:
        exists = False
        for new_project in plane_projects:
            if new_project["name"] == project["name"]:
                exists = True
                break
        if not exists :
            pprint.pp("Create new one " + project["name"])
        else:
            pprint.pp("Skip " + project["name"])

if __name__ == '__main__':
    plane_client = Plane.Client()
    pl_projects = plane_client.get_projects()
    #pprint.pp(result)
    #pprint.pp([prj["name"] for prj in pl_projects])

    openproject_client = OpenProject.Client()
    op_projects = openproject_client.get_projects()
    display.items_list([prj["name"] for prj in op_projects])
    #op_tasks = openproject_client.get_tasks()
    #pprint.pp([task["_links"]["project"]["title"] +
    # " - " + str(task["id"]) + task["subject"] for task in result])

    sync_projects(op_projects, pl_projects)

    #pprint.pp(result)

    # End script
    #display.end_info(start_date)
    display.deinit()
    sys.exit()
