import time
from colorama import Fore, Style
from src.util.logger import Logger
from src.database.db import AccountsDB

class RemoveMenuHandler:
    def __init__(self, manager):
        self.manager = manager   # Use the passed manager instead of creating a new instance
        self.logger = Logger()
        self.accounts_db = AccountsDB()
        self.menu_actions = {
            ".": self.manager.display_main_menu,  # "Go back" action
            "*": lambda: None
        }

    def remove_account(self, identifier):
        self.manager.print_logs_box()
        self.logger.log("INFO", "Removing account by ID")

        identifier_column = self.accounts_db.get_identifier_column(identifier)
        if not identifier_column:
            self.logger.log("ERROR", "Account not found!")
            time.sleep(1)
            return False

        self.accounts_db.remove_user(identifier_column, identifier)
        self.logger.log("INFO", "Account removed!")
        time.sleep(1)
        self.manager.display_remove_menu()
        return True

    def display_remove_menu(self):
        while True:
            self.logger.print_logo()
            accounts = self.accounts_db.get_all_users()
            print(f"{Fore.LIGHTCYAN_EX}*{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Remove Menu{Style.RESET_ALL}")
            menu = f"""
                {accounts}

                {Fore.LIGHTCYAN_EX}*{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Remove Menu{Style.RESET_ALL}
                
                {Fore.LIGHTCYAN_EX}id{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Remove account by ID{Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}.{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Go back{Style.RESET_ALL}
            """
            print(menu)
            option = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Option: {Style.RESET_ALL}").lower()

            # Check if the input is one of the menu actions
            if option in self.menu_actions:
                action = self.menu_actions.get(option)
                if action: action()
            # Assuming all ID's are numbers
            elif option.isdigit() and not self.remove_account(option):
                self.manager.print_logs_box()
                self.logger.log("ERROR", "Invalid id! Please try again.")
                time.sleep(1)
            else:
                self.manager.print_logs_box()
                self.logger.log("ERROR", "Invalid option! Please try again.")
                time.sleep(1)

