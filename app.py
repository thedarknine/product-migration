import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from utilities import display, logs, openproject, plane
from bullet import Bullet, colors

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

main_menu = [
    "OpenProject",
    "Plane",
    "Exit"
]
menu_options = [
    "List of projects",
    "List of types",
    "List of tasks",
    "List of users",
    "Back"
]

if __name__ == '__main__':
    answer = True
    while answer:
        platform = display.menu(main_menu)
        answer_platform = platform.launch()
        todo = display.menu(menu_options)
        answer = todo.launch()

        if answer_platform == "Exit":
            print("\n Goodbye") 
            answer = None
        
        elif answer_platform == "OpenProject":
            if answer == "List of projects":
                display.list(openproject.get_projects())
            elif answer == "List of types":
                display.list(openproject.get_types())
            elif answer == "List of tasks":
                tasks_list = openproject.get_tasks()
                print(len(tasks_list))
                #display.list(openproject.get_tasks())
            elif answer == "List of users":
                display.list(openproject.get_users())
            else:
                print("\n")
                answer = True

        elif answer_platform == "Plane":
            if answer == "List of projects":
                display.list(plane.get_projects())
            elif answer == "List of types":
                display.list(plane.get_types())
            elif answer == "List of users":
                display.list(plane.get_users())
            else:
                print("\n")
                answer = True

        elif answer=="Exit":
            print("\n Goodbye") 
            answer = None

        print("\n")

    display.end_info(start_date)
    display.deinit()
    exit()