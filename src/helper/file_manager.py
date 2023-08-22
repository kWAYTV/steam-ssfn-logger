import os
from src.util.logger import Logger
from src.helper.config import Config

defaultConfig = """
# Tool settings
username: "username_here"
manually_downloaded_ssfn_path: "C:\ssfn_downloads" # Path to manually downloaded ssfn file
"""

class FileManager():

    def __init__(self):
        self.logger = Logger()
        self.config = Config()
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
            exit()

    # Function to check if the input files are valid
    def check_input(self):

        # Check if the config file exists
        self.ensure_config()

        # Check if the database and rollback folders exist
        self.ensure_directory("src/database/container/")
        self.ensure_directory("src/util/rollback/")