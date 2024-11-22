import os
import colorama
from colorama import init, Fore, Back, Style
from datetime import datetime, timedelta

# MANAGE DISPLAY LIST ------------------------------------------------------------------------------- 
def list(list):
    if list:
        for item in list:
            print(colors('grey') + "• " + item)

# COLORS --------------------------------------------------------------------------------------------
def colors(name):
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
    print(colors('red') + "\n !!! \t" + message + colors('') + "\n")


def info(message):
    if not message == '':
        print(colors('') + message + "\n")


def title(message):
    print(Fore.YELLOW + "\n == " + message + " == " + colors(''))


# CLEARSCREEN ---------------------------------------------------------------------------------------
def clear_screen():
    colorama.init(autoreset=True)
    os.system('cls' if os.name == 'nt' else 'clear')


# DISPLAY START -------------------------------------------------------------------------------------
def start_info(start_date, title):
    print(colors('green') + "\n\n***************************************************************")
    print(colors('green') + "* " + title.upper())
    print(colors('green') + "***************************************************************\n")
    print(colors('cyan') + " • Lancement du script : " + start_date.strftime('%d/%m/%Y à %H:%M:%S'))
    print(colors('cyan') + "---------------------------------------------------------------\n" + colors(''))


# DISPLAY END ---------------------------------------------------------------------------------------
def end_info(start_date):
    end_date = datetime.now()
    print(colors('cyan') + "\n---------------------------------------------------------------")
    print(colors('cyan') + " • Fin du script : %s\n" % end_date.strftime('%d/%m/%Y à %H:%M:%S'))

    # Temps d'exécution total
    diff = end_date - start_date
    print(colors('yellow') + " ==> Temps d'exécution total : " + str(timedelta(seconds=diff.seconds)) + "\n\n")
