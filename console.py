import os
from colorama import Fore, Style

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def succes(s):
    return Fore.GREEN + s + Style.RESET_ALL

def question(s):
    return Style.BRIGHT + s + Style.RESET_ALL

def info(s):
    return Style.DIM + s + Style.RESET_ALL

def warning(s):
    return Fore.YELLOW + s + Style.RESET_ALL

def error(s):
    return Fore.RED + s + Style.RESET_ALL

def input_yesno(q):
    while True:
        answer = input(question(f"{q} y/n: ")).lower()
        if answer == "y" or answer == "yes":
            return "y"
        if answer == "n" or answer == "no":
            return "n"

def input_currency(prompt = "How much money do you want to deposit: "):
    full = 0
    cents = 0
    isValid = False
    while not isValid:
        raw_money = input(question(prompt))
        if "." in raw_money and len(raw_money.split(".")) == 2:
            full, cents = raw_money.split(".")
            try:
                full = int(full)
                if len(cents) == 1:
                    cents = int(cents) * 10
                elif len(cents) == 2:
                    cents = int(cents)
                else:
                    raise Exception
            except:
                pass
            else:
                if full >= 0 and cents >= 0:
                    isValid = True
        else:
            try:
                full = int(raw_money)
            except:
                pass
            else:
                if full >= 0:
                    isValid = True
    money = full * 100 + cents
    return money
