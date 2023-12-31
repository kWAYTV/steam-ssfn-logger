import yaml
from yaml import SafeLoader

class Config():
    def __init__(self):

        with open("config.yaml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)

            # Set the Build version & icon
            self.build_version: str = "1.5"

            self.username: str = self.config["username"]
            self.manually_downloaded_ssfn_path: str = self.config["manually_downloaded_ssfn_path"]
            self.rollback_path: str = self.config["rollback_path"]
            self.rollback_exe_path: str = self.config["rollback_exe_path"]

            self.github_url: str = self.config["github_url"]
            self.version_github_url: str = self.config["version_github_url"]
            self.steam_rollback_url: str = self.config["steam_rollback_url"]