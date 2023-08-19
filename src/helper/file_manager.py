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

    # Function to check if the input files are valid
    def check_input(self):

        # if there is no config file, create one.
        if not os.path.isfile("config.yaml"):
            self.logger.log("INFO", "Config file not found, creating one...")
            open("config.yaml", "w+").write(defaultConfig)
            self.logger.log("INFO", "Successfully created config.yml, please fill it out and try again.")
            exit()

        # if the folder /src/data/sessions/ doesn't exist, create it.
        if not os.path.isdir("src/database/container/"):
            self.logger.log("INFO", "Sessions folder not found, creating one...")
            os.mkdir("src/database/container/")

        # if the folder /src/util/rollback/ doesn't exist, create it.

        # if the folder "C:/ssfn_downloads" doesn't exist, create it.
        if not os.path.isdir(self.config.manually_downloaded_ssfn_path):
            self.logger.log("INFO", "Manually downloaded ssfn folder not found, creating one...")
            os.mkdir(self.config.get("manually_downloaded_ssfn_path"))