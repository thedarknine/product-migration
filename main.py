"""Main file for migration."""

import os
import sys
import toml
import arrow
from dotenv import load_dotenv
from sources.models.mapping import Mapping
from sources.models.project import Project
from sources.models.user import User
from sources.classes import plane as Plane, openproject as OpenProject, db as DB
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
include_statuses = mapping["plane"]["include_statuses"]

openproject_client = OpenProject.Client()
plane_client = Plane.Client()


def sync_projects(openproject_projects: list, plane_projects: list):
    """Check if project name exist into new tool.

    Args:
        openproject_projects (list): A list of projects.
        plane_projects (list): A list of projects.
    """
    return [
        project.name
        for project in openproject_projects
        if project.name not in [pl_project.name for pl_project in plane_projects]
    ]


def sync_statuses(plane_projects: list):
    """Check if status name exist into new tool.

    Args:
        plane_projects (list): A list of projects to get statuses.
    """
    for project in plane_projects:
        display.info("Update statuses for project " + project.name)
        statuses_list = plane_client.get_all_statuses_by_project(project.id)
        new_statuses = []
        for include_status in include_statuses:
            if include_status not in [status.name for status in statuses_list]:
                new_statuses.append(include_status)
                plane_client.create_status(project.id, include_status)
        display.items_list(new_statuses)


if __name__ == "__main__":
    logger.debug("Starting script")

    engine = DB.Client().connection()
    DB.Client().drop_schema(engine)
    DB.Client().create_schema(engine)

    tables_list = DB.Client().debug_tables_list(engine)
    display.items_list(tables_list)

    # Get projects to database
    projects_list = openproject_client.get_all_projects(exclude_op_projects)
    insert_projects = []
    for raw_project in projects_list:
        new_project = Project().from_raw(raw_project)
        insert_projects.append(new_project.to_dict())
    DB.Client().write_data(engine, "projects", insert_projects)

    # Get users to database
    users_list = openproject_client.get_all_users(exclude_op_users)
    insert_users = []
    for raw_user in users_list:
        new_user = User().from_raw(raw_user)
        insert_users.append(new_user.to_dict())
    DB.Client().write_data(engine, "users", insert_users)

    # Query DB
    # projects_list = DB.Client().read_data(engine, "projects")
    # print(projects_list)

    DB.Client().close_connection(engine)

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

    # display.title("OpenProject - Statuses")
    # display.items_list(
    #     [
    #         str(status.id) + " - " + status.name
    #         for status in openproject_client.get_all_statuses()
    #     ]
    # )

    # display.title("OpenProject - Types")
    # for project in openproject_client.get_all_projects(exclude_op_projects):
    #     display.info("Project: " + project.name)
    #     display.items_list(
    #         [
    #             str(issue_type.id) + " - " + issue_type.name
    #             for issue_type in openproject_client.get_all_types_by_project(
    #                 str(project.id)
    #             )
    #         ]
    #     )

    # display.title("OpenProject - Tasks")
    # tasks_list = []
    # for project in openproject_client.get_all_projects(exclude_op_projects):
    #     display.info("Project: " + project.name)
    #     tasks_list = []
    #     tasks_list = list(
    #         set(
    #             tasks_list
    #             + openproject_client.get_all_tasks_by_project(str(project.id))
    #         )
    #     )
    #     display.items_list([task.subject for task in tasks_list])
    #     display.info("=> Total tasks: " + str(len(tasks_list)) + "\n")

    # display.title("Plane - Projects")
    # display.items_list(
    #     [
    #         str(project.id) + " - " + project.name
    #         for project in plane_client.get_all_projects()
    #     ]
    # )

    # display.title("Plane - Users")
    # users_list = []
    # for project in plane_client.get_all_projects():
    #     # Merge lists
    #     users_list = list(
    #         set(
    #             users_list
    #             + plane_client.get_all_users_by_project(project.id, exclude_pl_users)
    #         )
    #     )
    # display.items_list([str(user.id) + " - " + user.email for user in users_list])

    # display.title("Plane - Tasks")
    # tasks_list = []
    # for project in plane_client.get_all_projects():
    #     display.info("Project: " + project.name)
    #     tasks_list = list(
    #         set(tasks_list + plane_client.get_all_tasks_by_project(project.id))
    #     )
    # display.items_list([task.name for task in tasks_list])

    ## TEST HULY self-hosted ======================================================================
    # Keep in mind that Huly doesn't support API calls and is based on MongoDB

    # display.title("Projects to create in Plane")
    # new_projects = sync_projects(
    #     openproject_client.get_all_projects(exclude_op_projects),
    #     plane_client.get_all_projects(),
    # )
    # display.items_list(new_projects)

    # sync_statuses(plane_client.get_all_projects())

    # End script
    display.end_info(start_date)
    sys.exit()
