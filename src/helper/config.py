import yaml
from yaml import SafeLoader

class Config():
    def __init__(self):

        with open("config.yaml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)

            # Set the Build version & icon
            self.build_version: str = "1.3.7"

            self.username: str = self.config["username"]
            self.manually_downloaded_ssfn_path: str = self.config["manually_downloaded_ssfn_path"]