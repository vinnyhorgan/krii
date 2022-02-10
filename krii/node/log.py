from colorama import Fore, Style
from datetime import datetime

def info(message):
    print(f"{datetime.now().strftime('%H:%M:%S')} {Fore.GREEN}INFO{Style.RESET_ALL}: {message}")

def warn(message):
    print(f"{datetime.now().strftime('%H:%M:%S')} {Fore.YELLOW}WARN{Style.RESET_ALL}: {message}")

def error(message):
    print(f"{datetime.now().strftime('%H:%M:%S')} {Fore.RED}ERROR{Style.RESET_ALL}: {message}")