"""
Terminal output utilitiy tools
"""
import os
from datetime import datetime, timedelta
import colorama
from colorama import Fore, Back, Style

# MANAGE DISPLAY LIST ------------------------------------------------------------------------------
def items_list(listing):
    """Display items of a list"""
    if listing:
        for item in listing:
            print(colors('grey') + "• " + item)

# COLORS -------------------------------------------------------------------------------------------
def colors(name):
    """Define colors system"""
    style = Style.RESET_ALL
    if name == "green":
        style = Fore.GREEN
    if name == "white":
        style = Back.WHITE
    if name == "red":
        style = Back.RED + Fore.BLACK
    if name == "cyan":
        style = Fore.CYAN + Style.DIM
    if name == "grey":
        style = Fore.BLACK
    if name == "yellow":
        style = Fore.YELLOW + Style.DIM
    return style

# MANAGE DISPLAY MESSAGE ---------------------------------------------------------------------------
def alert(message):
    """Display alert message"""
    print(colors('red') + "\n !!! \t" + message + colors('') + "\n")

def info(message):
    """Display info message"""
    if not message == '':
        print(colors('') + message + "\n")

def title(message):
    """Display section title"""
    print(Fore.YELLOW + "\n == " + message + " == " + colors(''))

# CLEARSCREEN --------------------------------------------------------------------------------------
def clear_screen():
    """Reset defined parameter"""
    colorama.init(autoreset=True)
    os.system('cls' if os.name == 'nt' else 'clear')

# DISPLAY START ------------------------------------------------------------------------------------
def start_info(start_date, script_title):
    """Display project title and start time"""
    print(colors('green') + "\n\n***************************************************************")
    print(colors('green') + "* " + script_title.upper())
    print(colors('green') + "***************************************************************\n")
    print(colors('cyan') + " • Lancement du script : " + start_date.strftime('%d/%m/%Y à %H:%M:%S'))
    print(colors('cyan') + "---------------------------------------------------------------\n")
    print(colors(''))

# DISPLAY END --------------------------------------------------------------------------------------
def end_info(start_date):
    """Display end time and duration"""
    end_date = datetime.now()
    print(colors('cyan') + "\n---------------------------------------------------------------")
    print(colors('cyan') + " • Fin du script : " + end_date.strftime('%d/%m/%Y à %H:%M:%S') + "\n")
    # Globale execution time
    diff = end_date - start_date
    print(colors('yellow') + " ==> Temps d'exécution total : "
          + str(timedelta(seconds=diff.seconds)) + "\n\n")

# DEINIT COLORAMA ----------------------------------------------------------------------------------
def deinit():
    """Remove colorama parameters"""
    colorama.deinit()
