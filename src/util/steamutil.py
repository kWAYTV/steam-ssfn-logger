import os, time, webbrowser
from src.util.logger import Logger
from src.steam.reg import SteamReg
from src.handler.ssfn import SSFNHandler

class SteamUtil:

    def __init__(self):
        self.logger = Logger()
        self.reg = SteamReg()
        self.ssfn = SSFNHandler()

    def get_steam_path(self):
        return self.reg.get_steam_path()
    
    def download_account_ssfn(self, ssfn):
        return self.ssfn.download(ssfn, self.get_steam_path())

    def autologin(self, username, password):
        steam_path = self.get_steam_path()
        steam_exe_path = os.path.join(steam_path, "steam.exe")
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
        self.logger.log("INFO", "Killing Steam...")
        kill_cmd = "taskkill /f /im steam.exe"
        os.system(kill_cmd)
        time.sleep(1)