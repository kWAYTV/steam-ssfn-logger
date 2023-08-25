import time
from getkey import getkey
from colorama import Fore, Style
from src.util.logger import Logger
from src.database.db import AccountsDB
from src.steam.session import SteamSession

class LogMenuHandler:
    def __init__(self, manager):
        self.manager = manager
        self.logger = Logger()
        self.accounts_db = AccountsDB()
        self.menu_actions = {
            ".": self.manager.display_main_menu,
            "*": lambda: None
        }
        self.steam_session = SteamSession(manager)

    def log_in_by_id(self, id):
        self.manager.print_logs_box()
        self.logger.log("INFO", "Logging in by ID")
        account = self.accounts_db.get_account("id", id)
        if account:
            self.logger.log("INFO", f"Logging in with account {account[1]}")
            self.steam_session.login(account[1], account[2], account[3])
            self.manager.display_main_menu()
            return True
        else:
            self.logger.log("ERROR", "Invalid ID!")
            time.sleep(1)
            self.manager.display_log_menu()
            return False

    def display_log_menu(self):
        while True:
            accounts = self.accounts_db.get_all_users()
            self.logger.print_logo()

            menu = f"""
                {accounts}

                {Fore.LIGHTCYAN_EX}*{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Log in Menu{Style.RESET_ALL}
                
                {Fore.LIGHTCYAN_EX}id{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Log in by id{Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}.{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Go back{Style.RESET_ALL}
            """
            print(menu)
            option = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Option: {Style.RESET_ALL}").lower()

            # Check if the input is one of the menu actions
            if option in self.menu_actions:
                action = self.menu_actions.get(option)
                if action: action()
            # Assuming all ID's are numbers
            elif option.isdigit() and not self.log_in_by_id(option):
                self.manager.print_logs_box()
                self.logger.log("ERROR", "Invalid id! Please try again.")
                time.sleep(1)
            else:
                self.manager.print_logs_box()
                self.logger.log("ERROR", "Invalid option! Please try again.")
                time.sleep(1)