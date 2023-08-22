import time
from getkey import getkey
from colorama import Fore, Style
from src.util.logger import Logger
from src.database.db import AccountsDB

class BanMenuHandler:
    def __init__(self, manager):
        self.manager = manager
        self.logger = Logger()
        self.accounts_db = AccountsDB()
        self.menu_actions = {
            "1": self.ban_account,
            "2": self.unban_account,
            ".": self.manager.display_main_menu,  # "Go back" action
            "*": lambda: None
        }

    def ban_account(self):
        self.manager.print_logs_box()
        self.logger.log("INFO", "Banning account")
        self.logger.log("INFO", "Account identifier (ID or username):")
        identifier = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Identifier: {Style.RESET_ALL}")

        identifier_column = self.accounts_db.get_identifier_column(identifier)
        if not identifier_column:
            self.logger.log("ERROR", "Account not found!")
            time.sleep(1)

        self.logger.log("INFO", "Account found! If you don't have for example weeks of ban, just type 0. This applies to all the values.")
        ban_durations = ["Weeks", "Days", "Hours", "Minutes"]
        values = {}

        for duration in ban_durations:
            while True:
                try:
                    self.logger.log("INPUT", f"{duration} of ban: ")
                    value = int(input(""))
                    values[duration.lower()] = value
                    break  # break the loop if the value is successfully parsed
                except ValueError:
                    self.logger.log("ERROR", f"Invalid input for {duration}. Please enter a number.")

        weeks, days, hours, minutes = values['weeks'], values['days'], values['hours'], values['minutes']

        self.accounts_db.add_ban(identifier_column, identifier, weeks=weeks, days=days, hours=hours, minutes=minutes)
        self.logger.log("INFO", "Account banned successfully!")
        time.sleep(1)
        self.manager.display_main_menu()

    def unban_account(self):

        self.manager.print_logs_box()
        self.logger.log("INFO", "Unbanning account")
        self.logger.log("INFO", "Account identifier (ID or username):")
        identifier = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Identifier: {Style.RESET_ALL}")

        identifier_column = self.accounts_db.get_identifier_column(identifier)
        if not identifier_column:
            self.logger.log("ERROR", "Account not found!")
            time.sleep(1)

        self.accounts_db.remove_ban(identifier_column, identifier)
        self.logger.log("INFO", "Account unbanned successfully!")
        time.sleep(1)
        self.manager.display_main_menu()

    def display_ban_menu(self):
        while True:
            self.logger.print_logo()
            accounts = self.accounts_db.get_all_users()
            print(f"{Fore.LIGHTCYAN_EX}*{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Ban Menu{Style.RESET_ALL}")
            
            menu = f"""
                {accounts}

                {Fore.LIGHTCYAN_EX}1{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Ban account{Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}2{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Unban account{Style.RESET_ALL}
                {Fore.LIGHTCYAN_EX}.{Fore.WHITE} -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Go back{Style.RESET_ALL}
            """
            print(menu)
            print(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Option: {Style.RESET_ALL}")
            option = getkey().lower()

            # Check if the input is one of the menu actions
            if option in self.menu_actions:
                action = self.menu_actions.get(option)
                if action: action()
            else:
                self.manager.print_logs_box()
                self.logger.log("ERROR", "Invalid option! Please try again.")
                time.sleep(1)