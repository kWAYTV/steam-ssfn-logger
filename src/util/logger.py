from os import system, name
from datetime import datetime
from colorama import Fore, Style
from src.helper.datetime import DateTime
from pystyle import Colors, Colorate, Center

logo = """
███████╗███████╗███████╗███╗   ██╗    ████████╗ ██████╗  ██████╗ ██╗     
██╔════╝██╔════╝██╔════╝████╗  ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
███████╗███████╗█████╗  ██╔██╗ ██║       ██║   ██║   ██║██║   ██║██║     
╚════██║╚════██║██╔══╝  ██║╚██╗██║       ██║   ██║   ██║██║   ██║██║     
███████║███████║██║     ██║ ╚████║       ██║   ╚██████╔╝╚██████╔╝███████╗
╚══════╝╚══════╝╚═╝     ╚═╝  ╚═══╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝"""

class Logger:

    def __init__(self):
        self.datetime_helper = DateTime()
        # Set the colors for the logs
        self.log_types = {
            "INFO": Fore.CYAN,
            "OK": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "UPDATER": Fore.YELLOW,
            "SLEEP": Fore.YELLOW,
            "ERROR": Fore.RED,
            "INPUT": Fore.BLUE,
        }

    # Clear console function
    def clear(self):
        system("cls" if name in ("nt", "dos") else "clear")

    def print_logo(self):
        self.clear()
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1)))
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "-----------------------------------------------------------\n\n", 1)))

    # Function to log messages to the console
    def log(self, type, message):
        color = self.log_types[type]
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y • %H:%M:%S")
        print(f"{Style.DIM}{current_time} • {Style.RESET_ALL}{Style.BRIGHT}{color}[{Style.RESET_ALL}{type}{Style.BRIGHT}{color}] {Style.RESET_ALL}{Style.BRIGHT}{Fore.WHITE}{message}")