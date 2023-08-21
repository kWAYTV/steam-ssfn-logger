import time
from colorama import Fore, Style
from src.util.logger import Logger
from src.database.db import AccountsDB
from src.steam.account import SteamAccount

class AddMenuHandler:
    def __init__(self, manager):
        self.manager = manager   # Use the passed manager instead of creating a new instance
        self.logger = Logger()
        self.account_fetcher = SteamAccount()
        self.accounts_db = AccountsDB()
        self.menu_actions = {
            "1": self.add_account_with_string,
            "2": self.add_account_step_by_step,
            ".": self.manager.display_main_menu,
            "*": lambda: None
        }

    def add_account_with_string(self):
        self.manager.print_logs_box()
        self.logger.log("INFO", "Adding account with entire string")
        account_input = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Account in format (username----password----ssfnXXXX or username:password:ssfnXXXX): {Style.RESET_ALL}")
        account = self.account_fetcher.fetch_account_by_string(account_input)
        if not self.accounts_db.account_exists("username", account[0]):
            self.accounts_db.add_user(account[0], account[1], account[2])
            self.logger.log("INFO", "Account added successfully!")
            time.sleep(1)
            self.manager.display_main_menu()
            return True
        else:
            self.logger.log("ERROR", "Account already exists!")
            time.sleep(1)
            self.manager.display_main_menu()
            return False

    def add_account_step_by_step(self):
        self.manager.print_logs_box()
        self.logger.log("INFO", "Adding account step by step")

        username = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Username: {Style.RESET_ALL}")
        password = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Password: {Style.RESET_ALL}")
        ssfn = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} SSFN: {Style.RESET_ALL}")

        if not self.accounts_db.account_exists("username", username):
            self.accounts_db.add_user(username, password, ssfn)
            self.logger.log("INFO", "Account added successfully!")
            time.sleep(1)
            self.manager.display_main_menu()
            return True
        else:
            self.logger.log("ERROR", "Account already exists!")
            time.sleep(1)
            self.manager.display_main_menu()
            return False

    def display_add_menu(self):
        while True:
            self.logger.print_logo()
            menu = f"""
                {Fore.LIGHTCYAN_EX}*{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Add Menu{Style.RESET_ALL}
                
                {Fore.LIGHTCYAN_EX}1{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Add account with entire string{Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}2{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Add account step by step{Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}.{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Go back{Style.RESET_ALL}
            """
            print(menu)
            option = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Option: {Style.RESET_ALL}").lower()

            action = self.menu_actions.get(option)
            if action: action()
            else:
                self.manager.print_logs_box()
                self.logger.log("ERROR", "Invalid option! Please try again.")
                time.sleep(1)