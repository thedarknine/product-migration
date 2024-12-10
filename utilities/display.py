"""
Terminal output utilitiy tools
"""

import os
from datetime import datetime, timedelta
import colorama
from colorama import Fore, Back, Style

STARRED_LINE = "***************************************************************"
DOTTED_LINE = "---------------------------------------------------------------"


# MANAGE DISPLAY LIST ------------------------------------------------------------------------------
def items_list(listing: list) -> None:
    """
    Display items of a list

    Args:
        listing (list): List of items
    """
    if listing and isinstance(listing, list):
        for item in listing:
            print(colors("grey") + "• " + item)


# COLORS -------------------------------------------------------------------------------------------
def colors(name: str) -> str:
    """
    Define colors system

    Args:
        name (str): Color name
    """
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
def alert(message: str) -> None:
    """
    Display alert message

    Args:
        message (str): Alert message
    """
    print(colors("red") + "\n !!! \t" + message + colors("") + "\n")


def info(message: str) -> None:
    """
    Display info message

    Args:
        message (str): Info message
    """
    if not message == "":
        print(colors("") + message + "\n")


def title(message: str) -> None:
    """
    Display section title

    Args:
        message (str): Section title
    """
    print(Fore.YELLOW + "\n == " + message + " == " + colors(""))


# CLEARSCREEN --------------------------------------------------------------------------------------
def clear_screen() -> None:
    """Reset defined parameter"""
    colorama.init(autoreset=True)
    os.system("cls" if os.name == "nt" else "clear")


# DISPLAY START ------------------------------------------------------------------------------------
def start_info(start_date: datetime, script_title: str) -> None:
    """
    Display project title and start time

    Args:
        start_date (datetime): Date and time with start of the script
        script_title (str): Script title
    """
    print(colors("green") + "\n\n" + STARRED_LINE)
    print(colors("green") + "* " + script_title.upper())
    print(colors("green") + STARRED_LINE + "\n")
    print(
        colors("cyan")
        + " • Lancement du script : "
        + start_date.strftime("%d/%m/%Y à %H:%M:%S")
    )
    print(colors("cyan") + DOTTED_LINE + "\n")
    print(colors(""))


# DISPLAY END --------------------------------------------------------------------------------------
def end_info(start_date: datetime) -> None:
    """
    Display end time and duration

    Args:
        start_date (datetime): Date and time with start of the script to compute duration
    """
    end_date = datetime.now()
    print(colors("cyan") + "\n" + DOTTED_LINE)
    print(
        colors("cyan")
        + " • Fin du script : "
        + end_date.strftime("%d/%m/%Y à %H:%M:%S")
        + "\n"
    )
    # Globale execution time
    diff = end_date - start_date
    print(
        colors("yellow")
        + " ==> Temps d'exécution total : "
        + str(timedelta(seconds=diff.seconds))
        + "\n\n"
    )


# DEINIT COLORAMA ----------------------------------------------------------------------------------
def deinit():
    """Remove colorama parameters"""
    colorama.deinit()
