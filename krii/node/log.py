from colorama import Fore, Style
from datetime import datetime

to_file = False

def info(message):
    print(f"{datetime.now().strftime('%H:%M:%S')} {Fore.GREEN}INFO{Style.RESET_ALL}: {message}")

    if to_file:
        f = open("log.txt", "a")
        f.write(f"{datetime.now().strftime('%H:%M:%S')} INFO: {message}\n")
        f.close()

def warn(message):
    print(f"{datetime.now().strftime('%H:%M:%S')} {Fore.YELLOW}WARN{Style.RESET_ALL}: {message}")

    if to_file:
        f = open("log.txt", "a")
        f.write(f"{datetime.now().strftime('%H:%M:%S')} WARN: {message}\n")
        f.close()

def error(message):
    print(f"{datetime.now().strftime('%H:%M:%S')} {Fore.RED}ERROR{Style.RESET_ALL}: {message}")

    if to_file:
        f = open("log.txt", "a")
        f.write(f"{datetime.now().strftime('%H:%M:%S')} ERROR: {message}\n")
        f.close()