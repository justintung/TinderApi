from colorama import Fore, init, Style
from datetime import datetime


init(autoreset=True)

class Debugger():
    def __init__(self, debug=False) -> None:
        self.debug = debug
        self.cyan = Fore.CYAN
        self.magenta = Fore.MAGENTA
        self.reset = Fore.RESET

    def Log(self, message):
        if self.debug:
            print(f"{self.cyan}{self.getTime()} {self.magenta}{message}{self.reset}")

    def getTime(self):
        now = datetime.now()
        return now.strftime("%H:%M:%S")