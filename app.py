import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from utilities import display, logs, openproject, plane

display.clear_screen()

# Load env variables
try:
    load_dotenv(os.getenv("PROJECT_NAME"))
except (ValueError, Exception):
    sys.exit(display.alert("Configuration could not be loaded (" + repr(Exception) + ")"))

# Initialize logs
logs.init_file()

start_date = datetime.now()
display.start_info(start_date, 'Migration')

if __name__ == '__main__':
    answer = True
    while answer:
        print("""
        10. List of projects in OpenProject
        11. List of types in OpenProject
        12. List of tasks in OpenProject
        13. List of users in OpenProject
        20. List of projects in Plane
        21. List of types in Plane
        22. List of users in Plane
        30. Exit/Quit
        """)
        answer=input("What would you like to do? ")

        if answer=="10":
            print("\nList of projects in OpenProject")
            display.list(openproject.get_projects())
        elif answer=="11":
            print("\nList of types in OpenProject")
            display.list(openproject.get_types())
        elif answer=="12":
            print("\nList of tasks in OpenProject")
            tasks_list = openproject.get_tasks()
            print(len(tasks_list))
            #display.list(openproject.get_tasks())
        elif answer=="13":
            print("\nList of users in OpenProject")
            display.list(openproject.get_users())
        elif answer=="20":
            print("\nList of projects in Plane")
            display.list(plane.get_projects())
        elif answer=="21":
            print("\nList of types in Plane")
            display.list(plane.get_types())
        elif answer=="22":
            print("\nList of users in Plane")
            display.list(plane.get_users())
        elif answer=="30":
            print("\n Goodbye") 
            answer = None
        else:
            print("\n Not Valid Choice Try again")

    display.end_info(start_date)

    display.deinit()
    exit()