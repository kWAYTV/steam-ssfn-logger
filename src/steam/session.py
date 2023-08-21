import os
from src.util.logger import Logger
from src.helper.config import Config
from src.util.steamutil import SteamUtil

class SteamSession:
    def __init__(self, manager):
        self.config = Config()
        self.logger = Logger()
        self.steam_util = SteamUtil()
        self.menu_manager = manager
    
    def login(self, username, password, ssfn):
        self.steam_util.shutdown_steam()
        self.steam_util.download_account_ssfn(ssfn)
        self.steam_util.autologin(username, password)
        self.menu_manager.display_main_menu()