import requests, os, time
from src.util.logger import Logger
from src.helper.config import Config

class SteamRollback:
    def __init__(self):
        self.logger = Logger()
        self.config = Config()
        self.session = requests.session()

    def download_rollback(self):
        self.logger.log("ROLLBACK", "Deleting old files...")
        for file in os.listdir(self.config.rollback_path):
            os.remove(os.path.join(self.config.rollback_path, file))
        
        self.logger.log("ROLLBACK", "Downloading the tool...")
        response = self.session.get(self.config.steam_rollback_url, allow_redirects=True)
        if response.content:
            with open(self.config.rollback_exe_path, "wb") as f:
                f.write(response.content)
                self.logger.log("ROLLBACK", "Successfully downloaded the rollback tool.")
                time.sleep(1)
                return True
        else:
            self.logger.log("ERROR", "Failed to download the rollback tool!")
            time.sleep(1)
            return False

    def start_rollback_exe(self):
        self.logger.log("ROLLBACK", "Starting tool...")
        os.system(f'start "Rollback by https://github.com/IMXNOOBX" {self.config.rollback_exe_path}')

    def execute_rollback(self):
        self.logger.log("ROLLBACK", "Executing the rollback tool...")
        if os.path.exists(self.config.rollback_exe_path):
            self.logger.log("ROLLBACK", "Rollback tool found, executing...")
            self.start_rollback_exe()
        else:
            self.logger.log("ERROR", "Rollback tool not found, downloading...")
            self.download_rollback()
            self.execute_rollback()