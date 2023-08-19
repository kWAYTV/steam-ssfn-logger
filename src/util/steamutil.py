import os, time
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

    def kill_steam(self):
        self.logger.log("INFO", "Killing Steam...")
        os.system("taskkill /f /im steam.exe")
        time.sleep(1)
    
    def download_account_ssfn(self, ssfn):
        return self.ssfn.download(ssfn, self.get_steam_path())

    def autologin(self, username, password):
        steam_path = self.get_steam_path()
        steam_exe_path = os.path.join(steam_path, "steam.exe")
        launch_command = f'"{steam_exe_path}" -noreactlogin -rememberlogin -rememberpassword -login {username} {password}'
        os.system(f'start "CSGO" {launch_command}')