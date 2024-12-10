"""
Terminal output utilitiy tools
"""

import os
from datetime import timedelta
import arrow
from rich.console import Console
from rich.style import Style

STARRED_LINE = "***************************************************************"
DOTTED_LINE = "---------------------------------------------------------------"

# COLORS -------------------------------------------------------------------------------------------
console = Console()
danger_style = Style(color="red1", blink=True)
green_style = Style(color="green")
white_style = Style(color="white")
cyan_style = Style(color="cyan")
yellow_style = Style(color="gold1")
grey_style = Style(color="bright_black")


# MANAGE DISPLAY LIST ------------------------------------------------------------------------------
def items_list(listing: list) -> None:
    """
    Display items of a list

    Args:
        listing (list): List of items
    """
    if listing and isinstance(listing, list):
        for item in listing:
            console.print("• " + item, style=grey_style)


# MANAGE DISPLAY MESSAGE ---------------------------------------------------------------------------
def alert(message: str) -> None:
    """
    Display alert message

    Args:
        message (str): Alert message
    """
    console.print("\n !!! \t" + message + "\n", style=danger_style)


def info(message: str) -> None:
    """
    Display info message

    Args:
        message (str): Info message
    """
    if not message == "":
        console.print(message + "\n")


def title(message: str) -> None:
    """
    Display section title

    Args:
        message (str): Section title
    """
    console.print("\n == " + message + " == ", style=yellow_style)


# CLEARSCREEN --------------------------------------------------------------------------------------
def clear_screen() -> None:
    """Reset defined parameter"""
    os.system("cls" if os.name == "nt" else "clear")


# DISPLAY START ------------------------------------------------------------------------------------
def start_info(start_date: arrow, script_title: str) -> None:
    """
    Display project title and start time

    Args:
        start_date (arrow): Date and time with start of the script
        script_title (str): Script title
    """
    console.print("\n\n" + STARRED_LINE, style=green_style)
    console.print("* " + script_title.upper(), style=green_style)
    console.print(STARRED_LINE + "\n", style=green_style)
    console.print(
        " • Lancement du script : " + start_date.format("DD/MM/YYYY à HH:mm:ss"),
        style=cyan_style,
    )
    console.print(DOTTED_LINE + "\n", style=cyan_style)


# DISPLAY END --------------------------------------------------------------------------------------
def end_info(start_date: arrow) -> None:
    """
    Display end time and duration

    Args:
        start_date (arrow): Date and time with start of the script to compute duration
    """
    end_date = arrow.now(os.getenv("TIMEZONE", "Europe/Paris"))
    console.print("\n" + DOTTED_LINE, style=cyan_style)
    console.print(
        " • Fin du script : " + end_date.format("DD/MM/YYYY à HH:mm:ss") + "\n",
        style=cyan_style,
    )
    # Globale execution time
    diff = end_date - start_date
    console.print(
        " ==> Temps d'exécution total : "
        + str(timedelta(seconds=diff.seconds))
        + "\n\n",
        style=yellow_style,
    )
