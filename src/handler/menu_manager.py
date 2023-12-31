import os
from pystyle import Center
from colorama import Fore, Style
from src.helper.config import Config
from src.handler.log_menu import LogMenuHandler
from src.handler.add_menu import AddMenuHandler
from src.handler.main_menu import MainMenuHandler
from src.handler.remove_menu import RemoveMenuHandler
from src.handler.ban_menu import BanMenuHandler

class MenuManager:
    def __init__(self):
        self.main_menu_handler = MainMenuHandler(self)
        self.add_menu_handler = AddMenuHandler(self)
        self.log_menu_handler = LogMenuHandler(self)
        self.remove_menu_handler = RemoveMenuHandler(self)
        self.ban_menu_handler = BanMenuHandler(self)
        # Set title
        os.system(f"title SSFN Logger Tool {Config().build_version} - Main Menu - kwayservices.top")

    def display_main_menu(self):
        os.system(f"title SSFN Logger Tool {Config().build_version} - Main Menu - kwayservices.top")
        self.main_menu_handler.display_main_menu()

    def display_add_menu(self):
        os.system(f"title SSFN Logger Tool {Config().build_version} - Add Account Menu - kwayservices.top")
        self.add_menu_handler.display_add_menu()

    def display_remove_menu(self):
        os.system(f"title SSFN Logger Tool {Config().build_version} - Remove Account Menu - kwayservices.top")
        self.remove_menu_handler.display_remove_menu()

    def display_log_menu(self):
        os.system(f"title SSFN Logger Tool {Config().build_version} - Log in Menu - kwayservices.top")
        self.log_menu_handler.display_log_menu()

    def display_ban_menu(self):
        os.system(f"title SSFN Logger Tool {Config().build_version} - Ban Account Menu - kwayservices.top")
        self.ban_menu_handler.display_ban_menu()

    def print_logs_box(self):
        os.system(f"title SSFN Logger Tool {Config().build_version} - Showing logs - kwayservices.top")
        print(Center.XCenter(f"\n\n{Fore.LIGHTCYAN_EX}[{Fore.WHITE}LOGS{Fore.LIGHTCYAN_EX}]{Style.RESET_ALL}\n\n"))
