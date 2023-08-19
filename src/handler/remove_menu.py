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

    def exit_program(self):
        self.manager.print_logs_box()
        self.logger.log("INFO", "Exiting...")
        exit()

    def remove_account_by_id(self, id):
        self.manager.print_logs_box()
        self.logger.log("INFO", "Removing account by ID")

        if self.accounts_db.account_exists_by_id(id):
            self.accounts_db.remove_user_by_id(id)
            self.logger.log("INFO", "Account removed successfully!")
            time.sleep(1)
            self.manager.display_main_menu()
        else:
            self.logger.log("ERROR", "Account not found!")
            time.sleep(1)
            self.manager.display_main_menu()

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
            # Assuming all ID's are numbers, if not you may need to adjust this check
            elif option.isdigit():
                # If not a menu action, attempt to remove the account with the provided ID
                self.remove_account_by_id(option)
            else:
                self.manager.print_logs_box()
                self.logger.log("ERROR", "Invalid option or ID! Please try again.")
                time.sleep(1)

