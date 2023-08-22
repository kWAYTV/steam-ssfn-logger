import os, time, webbrowser
from src.util.logger import Logger
from src.steam.reg import SteamReg
from src.database.db import AccountsDB
from src.handler.ssfn import SSFNHandler

class SteamUtil:

    def __init__(self):
        self.logger = Logger()
        self.reg = SteamReg()
        self.ssfn = SSFNHandler()
        self.accounts_db = AccountsDB()

    def download_account_ssfn(self, ssfn):
        return self.ssfn.download(ssfn, self.reg.get_steam_path())

    def autologin(self, username, password):
        steam_exe_path = self.reg.get_steam_exe_path()
        launch_command = f'"{steam_exe_path}" -noreactlogin -rememberlogin -rememberpassword -login {username} {password}'
        os.system(f'start "CSGO" {launch_command}')

    def execute_rollback(self):
        self.logger.log("INFO", "Executing Steam Rollback/Unroll...")
        rollback_cmd = "src/util/rollback/steam-rollback.exe"
        if os.path.exists(rollback_cmd):
            os.system(f'start "Rollback by https://github.com/IMXNOOBX" {rollback_cmd}')
        else:
            self.logger.log("ERROR", f"{rollback_cmd} does not exist! Opening download link...")
            webbrowser.open("https://github.com/IMXNOOBX/steam-rollback/releases")
            time.sleep(1)

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