import os
import colorama
from colorama import init, Fore, Back, Style
from datetime import datetime, timedelta
from bullet import Bullet, colors

# MANAGE DISPLAY LIST ------------------------------------------------------------------------------- 
def list(list):
    if list:
        for item in list:
            print(custom_colors('grey') + "• " + item)

# COLORS --------------------------------------------------------------------------------------------
def custom_colors(name):
    if name == "green":
        return Fore.GREEN
    elif name == "white":
        return Back.WHITE
    elif name == "red":
        return Back.RED + Fore.BLACK
    elif name == "cyan":
        return Fore.CYAN + Style.DIM
    elif name == "grey":
        return Fore.BLACK
    elif name == "yellow":
        return Fore.YELLOW + Style.DIM
    else:
        return Style.RESET_ALL


# MANAGE DISPLAY MESSAGE ----------------------------------------------------------------------------
def alert(message):
    print(custom_colors('red') + "\n !!! \t" + message + custom_colors('') + "\n")


def info(message):
    if not message == '':
        print(custom_colors('') + message + "\n")


def title(message):
    print(Fore.YELLOW + "\n == " + message + " == " + custom_colors(''))


# MANAGE DISPLAY MENU -------------------------------------------------------------------------------
def menu(options):
    return Bullet(
        prompt = "What would you like to do? ",
        choices = options,
        indent = 0,
        align = 5,
        margin = 2,
        shift = 0,
        bullet = "➜",
        bullet_color = colors.foreground["green"],
        word_on_switch=colors.foreground["green"],
        background_on_switch=colors.background["green"],
        pad_right = 5
    )

# CLEARSCREEN ---------------------------------------------------------------------------------------
def clear_screen():
    colorama.init(autoreset=True)
    os.system('cls' if os.name == 'nt' else 'clear')


# DISPLAY START -------------------------------------------------------------------------------------
def start_info(start_date, title):
    print(custom_colors('green') + "\n\n***************************************************************")
    print(custom_colors('green') + "* " + title.upper())
    print(custom_colors('green') + "***************************************************************\n")
    print(custom_colors('cyan') + " • Lancement du script : " + start_date.strftime('%d/%m/%Y à %H:%M:%S'))
    print(custom_colors('cyan') + "---------------------------------------------------------------\n" + custom_colors(''))


# DISPLAY END ---------------------------------------------------------------------------------------
def end_info(start_date):
    end_date = datetime.now()
    print(custom_colors('cyan') + "\n---------------------------------------------------------------")
    print(custom_colors('cyan') + " • Fin du script : %s\n" % end_date.strftime('%d/%m/%Y à %H:%M:%S'))

    # Temps d'exécution total
    diff = end_date - start_date
    print(custom_colors('yellow') + " ==> Temps d'exécution total : " + str(timedelta(seconds=diff.seconds)) + "\n\n")

# DEINIT COLORAMA -----------------------------------------------------------------------------------
def deinit():
    colorama.deinit()