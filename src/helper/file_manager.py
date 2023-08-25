import os
from src.util.logger import Logger

defaultConfig = """
# Tool settings
username: username_here
manually_downloaded_ssfn_path: "C:/ssfn_downloads" # Path to manually downloaded ssfn file
rollback_path: "src/util/rollback" # Path to steam rollback folder
rollback_exe_path: "src/util/rollback/steam-rollback.exe" # Path to steam-rollback.exe

# Github urls
github_url: https://github.com/kWAYTV/steam-ssfn-logger
version_github_url: https://raw.githubusercontent.com/kWAYTV/steam-ssfn-logger/main/src/helper/config.py
steam_rollback_url: https://github.com/IMXNOOBX/steam-rollback/releases/download/steam-rollback/steam-rollback.exe
"""

class FileManager():

    def __init__(self):
        self.logger = Logger()
        # Check if the files are there
        self.check_input()

    def ensure_directory(self, path):
        """Ensure that a directory exists. If it doesn't, create it."""
        if not os.path.isdir(path):
            try:
                self.logger.log("INFO", f"{path} folder not found, creating one...")
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                self.logger.log("ERROR", f"Failed to create directory {path}. Error: {e}")

    def ensure_config(self):
        """Ensure that the config file exists. If it doesn't, create it."""
        if not os.path.isfile("config.yaml"):
            self.logger.log("INFO", "Config file not found, creating one...")
            open("config.yaml", "w+").write(defaultConfig)
            self.logger.log("INFO", "Successfully created config.yml, please fill it out and try again.")
            self.logger.exit_program()

    # Function to check if the input files are valid
    def check_input(self):

        # Check if the config file exists
        self.ensure_config()

        # Check if the database and rollback folders exist
        self.ensure_directory("src/database/container/")
        self.ensure_directory("src/util/rollback/")