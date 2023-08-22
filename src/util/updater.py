import requests, re, webbrowser
from colorama import Fore
from src.util.logger import Logger
from src.helper.config import Config

class Updater:

    def __init__(self):
        self.logger = Logger()
        self.config = Config()

    def check_update(self):
        # Check for updates
        if self.check_versions():
            option = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Are you sure you want to continue without updating? [y/n]")
            if option.lower() == "n":
                webbrowser.open(self.config.github_url)
                exit()
            if option.lower() == "y":
                pass
            else:
                self.logger.log("ERROR", "Invalid option!")
                exit()
        else:
            pass

    def check_versions(self):
        """Check for updates by comparing local build version with GitHub's build version."""

        self.logger.print_logo()
        self.logger.log("UPDATER", "Checking for updates...")
        # Fetch the config.py from GitHub
        response = requests.get(self.config.version_github_url)
        
        if response.status_code == 200:
            # Extract the build_version from fetched file using regex
            version_match = re.search(r'self.build_version: str = "([\d\.]+)"', response.text)
            
            if version_match:
                github_version = version_match.group(1)
                local_version = self.config.build_version
                
                if github_version == local_version:
                    self.logger.log("UPDATER", "You are using the latest version.")
                    return False
                else:
                    self.logger.log("UPDATER", f"Update available! Latest version: {github_version} - Your version: {local_version}")
                    return True
            else:
                self.logger.log("UPDATER", "Failed to extract version from GitHub. Please check manually.")
                return False
        else:
            self.logger.log("UPDATER", "Failed to fetch updates from GitHub. Please check your internet connection.")
            return False