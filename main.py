"""Main file for migration."""

import os
import sys
import pprint
import toml
import arrow
from dotenv import load_dotenv
from sources.models.mapping import Mapping
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

# Load mapping configuration
try:
    mapping = toml.load("mapping.toml")
    Mapping.model_validate(mapping)
except toml.TomlDecodeError as e:
    print(f"TOML file is invalid: {e}")
exclude_op_projects = mapping["openproject"]["exclude_projects"]
exclude_op_users = mapping["openproject"]["exclude_users"]
exclude_pl_projects = (
    mapping["plane"]["exclude_projects"]
    if "exclude_projects" in mapping["plane"]
    else []
)
exclude_pl_users = mapping["plane"]["exclude_users"]


def sync_projects(openproject_projects: list, plane_projects: list):
    """Check if project name exist into new tool.

    Args:
        openproject_projects (list): A list of projects.
        plane_projects (list): A list of projects.
    """
    for tmp_project in openproject_projects:
        exists = False
        for new_project in plane_projects:
            if new_project["name"] == tmp_project["name"]:
                exists = True
                break
        if not exists:
            pprint.pp("Create new one " + tmp_project["name"])
        else:
            pprint.pp("Skip " + tmp_project["name"])


if __name__ == "__main__":
    logger.debug("Starting script")
    openproject_client = OpenProject.Client()
    plane_client = Plane.Client()

    # display.title("OpenProject - Projects")
    # display.items_list(
    #     [str(project.id) + " - " + project.name
    #       for project in openproject_client.get_all_projects(exclude_op_projects)]
    # )

    # display.title("OpenProject - Users")
    # display.items_list(
    #     [
    #         str(user.id) + " - " + user.email
    #         for user in openproject_client.get_all_users(exclude_op_users)
    #     ]
    # )

    display.title("Plane - Projects")
    display.items_list(
        [
            str(project.id) + " - " + project.name
            for project in plane_client.get_all_projects()
        ]
    )

    display.title("Plane - Users")
    users_list = []
    for project in plane_client.get_all_projects():
        # Merge lists
        users_list = list(
            set(
                users_list
                + plane_client.get_all_users_by_project(project.id, exclude_pl_users)
            )
        )
    display.items_list([str(user.id) + " - " + user.email for user in users_list])

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
    # op_users = openproject_client.get_all(os.getenv("OPENPROJECT_PATH_USERS"))
    # display.items_list([usr["email"] for usr in op_users])
    # op_tasks = openproject_client.get_tasks()
    # pprint.pp([task["_links"]["project"]["title"] +
    # " - " + str(task["id"]) + task["subject"] for task in op_tasks])

    # sync_projects(op_projects, pl_projects)

    # End script
    display.end_info(start_date)
    sys.exit()
