import winreg

class SteamReg:
    def __init__(self):
        self.reg_path = r"SOFTWARE\Valve\Steam"

    def get_steam_path(self):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.reg_path) as key:
            return winreg.QueryValueEx(key, 'SteamPath')[0]

    def get_steam_exe_path(self):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.reg_path) as key:
            return winreg.QueryValueEx(key, 'SteamExe')[0]