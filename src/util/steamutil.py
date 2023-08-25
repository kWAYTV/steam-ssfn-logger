import os, time, webbrowser
from src.util.logger import Logger
from src.steam.reg import SteamReg
from src.database.db import AccountsDB
from src.handler.ssfn import SSFNHandler
from src.util.rollback import SteamRollback

class SteamUtil:

    def __init__(self):
        self.logger = Logger()
        self.reg = SteamReg()
        self.ssfn = SSFNHandler()
        self.accounts_db = AccountsDB()
        self.rollback = SteamRollback()

    def download_account_ssfn(self, ssfn):
        return self.ssfn.download_server(ssfn, self.reg.get_steam_path())

    def autologin(self, username, password):
        steam_exe_path = self.reg.get_steam_exe_path()
        launch_command = f'"{steam_exe_path}" -noreactlogin -rememberlogin -rememberpassword -login {username} {password}'
        os.system(f'start "CSGO" {launch_command}')

    def execute_rollback(self):
        self.rollback.execute_rollback()

    def kill_steam(self):
        try:
            self.logger.log("INFO", "Killing Steam...")
            kill_cmd = "taskkill /f /im steam.exe"
            os.system(kill_cmd)
            time.sleep(1)
        except Exception as e:
            self.logger.log("ERROR", f"Error killing Steam: {e} (Did you run as administrator?)")
            time.sleep(1)

    def shutdown_steam(self):
        self.logger.log("INFO", "Shutting down Steam...")
        steam_exe_path = self.reg.get_steam_exe_path()
        shutdown_cmd = f'"{steam_exe_path}" -shutdown'
        os.system(shutdown_cmd)
        time.sleep(1)

    def import_old_db(self):
        self.logger.log("INFO", "Importing old database...")
        self.accounts_db.import_from_old_db()
        time.sleep(1)