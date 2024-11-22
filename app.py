import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from utilities import display, logs, openproject

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
        1. List of projects in OpenProject
        2. Exit/Quit
        """)
        answer=input("What would you like to do? ")

        if answer=="1":
            print("\nList of projects in OpenProject")
            display.list(openproject.get_projects())
        elif answer=="2":
            print("\n Goodbye") 
            answer = None
        else:
            print("\n Not Valid Choice Try again")

    display.end_info(start_date)

    display.deinit()
    exit()