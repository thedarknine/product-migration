import sys
from dotenv import load_dotenv
from utilities import display, logs

display.clear_screen()

# Load env variables
try:
    load_dotenv()
except (ValueError, Exception):
    sys.exit(display.alert("Configuration could not be loaded (" + repr(Exception) + ")"))

# Initialize logs
logs.init_file()

if __name__ == '__main__':
    display.alert('Hello World')