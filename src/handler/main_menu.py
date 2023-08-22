import time, webbrowser
from getkey import getkey
from colorama import Fore, Style
from src.util.logger import Logger
from src.util.steamutil import SteamUtil

class MainMenuHandler:
    def __init__(self, manager):
        self.manager = manager   # Use the passed manager instead of creating a new instance
        self.logger = Logger()
        self.steam_util = SteamUtil()
        self.menu_actions = {
            "1": self.manager.display_log_menu,
            "2": self.manager.display_add_menu,
            "3": self.manager.display_remove_menu,
            "4": self.manager.display_ban_menu,
            "5": self.steam_util.kill_steam,
            "6": self.steam_util.import_old_db,
            "7": self.steam_util.execute_rollback,
            ".": self.exit_program,
            "*": lambda: None
        }

    def exit_program(self):
        self.manager.print_logs_box()
        self.logger.log("INFO", "Bye!")
        exit()

    def open_website(self):
        webbrowser.open("https://kwayservices.top")

    def display_main_menu(self):
        while True:
            self.logger.print_logo()
            menu = f"""
                {Fore.LIGHTCYAN_EX}*{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Main Menu{Style.RESET_ALL}
                
                {Fore.LIGHTCYAN_EX}1{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Log in{Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}2{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Add account(s){Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}3{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Remove account(s){Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}4{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Ban/Unban account(s){Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}5{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Kill Steam processe(s){Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}6{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Import users from old database{Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}7{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} One-click Steam Rollback/Unroll{Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}.{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Exit{Style.RESET_ALL}
            """
            print(menu)
            print(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Option: {Style.RESET_ALL}")
            option = getkey().lower()

            action = self.menu_actions.get(option)
            if action: action()
            else:
                self.manager.print_logs_box()
                self.logger.log("ERROR", "Invalid option! Please try again.")
                time.sleep(1)