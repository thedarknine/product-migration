"""
Main file for migration
"""

import os
import sys
import pprint
import arrow
from dotenv import load_dotenv
from sources.models.mapping import Mapping
from sources.models.openproject import Project as OPProject
from sources.models.plane import Project as PlProject
from sources.classes import plane as Plane, openproject as OpenProject
from sources.utilities import display, logs

# Load env variables
try:
    load_dotenv(os.getenv("PROJECT_NAME"))
except FileNotFoundError:
    sys.exit(display.alert(f"Configuration could not be loaded {repr(Exception)}"))

display.clear_screen()

# Initialize logs
logger = logs.init_logger()

# Initialize script info
start_date = arrow.now(os.getenv("TIMEZONE", "Europe/Paris"))
display.start_info(start_date, "Migration")


def sync_projects(openproject_projects, plane_projects):
    """Check if project name exist into new tool"""
    for project in openproject_projects:
        exists = False
        for new_project in plane_projects:
            if new_project["name"] == project["name"]:
                exists = True
                break
        if not exists:
            pprint.pp("Create new one " + project["name"])
        else:
            pprint.pp("Skip " + tmp_project["name"])


def get_op_projects():
    """
    Get all projects from OpenProject.

    Returns
    -------
    list
        A list of projects.
    """
    openproject_client = OpenProject.Client()
    op_projects_result = openproject_client.get_all(
        os.getenv("OPENPROJECT_PATH_PROJECTS")
    )
    op_projects_list = openproject_client.compute_projects(
        op_projects_result, exclude_op_projects
    )
    return [OPProject.model_validate(project) for project in op_projects_list]


def get_pl_projects():
    """
    Get all projects from Plane.

    Returns
    -------
    list
        A list of projects.
    """
    plane_client = Plane.Client()
    pl_projects = plane_client.get_all(os.getenv("PLANE_PATH_PROJECTS"))
    pl_projects_list = plane_client.compute_projects(pl_projects, exclude_op_projects)
    return [PlProject.model_validate(project) for project in pl_projects_list]


if __name__ == "__main__":
    logger.debug("Starting script")

    display.title("OpenProject - Projects")
    display.items_list(
        [str(project.id) + " - " + project.name for project in get_op_projects()]
    )

    display.title("OpenProject - Users")

    display.title("Plane - Projects")
    display.items_list(
        [str(project.id) + " - " + project.name for project in get_pl_projects()]
    )

    # for project in pl_projects_list:
    #     pl_users_result = plane_client.get_all(
    #           os.getenv("PLANE_PATH_USERS"), "{PROJECT_ID}", project["id"]
    #     )
    #     pl_users_list = plane_client.compute_users(pl_users_result, exclude_pl_users)
    #     display.items_list([project["id"] +
    #                         " - " + str(user["id"]) + " " +
    #                         user["email"] for user in pl_users_list])
    #     del pl_users_result

    # display.items_list([project["name"] for project in op_projects_list])
    # total_tasks = 0
    # for project in op_projects_list:
    #     op_tasks_list = openproject_client.get_tasks_by_projectid(project["id"])
    #     total_tasks += len(op_tasks_list)
    #     display.items_list([task["_links"]["project"]["title"] +
    #                         " - " + str(task["id"]) + " " +
    #                         task["subject"] for task in op_tasks_list])
    #     display.info(project["name"] + " -> Total tasks : " + str(len(op_tasks_list)))
    #     # break
    # display.info("Total tasks : " + str(total_tasks))
    # op_projects = openproject_client.get_projects()
    # display.items_list([prj["name"] for prj in op_projects])
    # op_users = openproject_client.get_users()
    # display.items_list([usr["email"] for usr in op_users])
    # op_tasks = openproject_client.get_tasks()
    # pprint.pp([task["_links"]["project"]["title"] +
    # " - " + str(task["id"]) + task["subject"] for task in result])

    # sync_projects(op_projects, pl_projects)

    # pprint.pp(result)

    # End script
    display.end_info(start_date)
    sys.exit()
