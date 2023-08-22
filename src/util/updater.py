import requests, re, webbrowser, time
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
            option = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Are you sure you want to continue without updating? [y/n] ")
            if option.lower() == "n":
                self.logger.log("INFO", "Opening GitHub page...")
                webbrowser.open(self.config.github_url)
                time.sleep(1)
                exit()
            if option.lower() == "y":
                self.logger.log("INFO", "Continuing without updating...")
                time.sleep(1)
                pass
            else:
                self.logger.log("ERROR", "Invalid option!")
                time.sleep(1)
                exit()
        else:
            pass

    def check_versions(self):
        """Check for updates by comparing local build version with GitHub's build version."""

        self.logger.print_logo()
        self.logger.log("UPDATER", "Checking for updates...")

        response = requests.get(self.config.version_github_url)
        if response.status_code == 200:
            version_match = re.search(r'self.build_version: str = "([\d\.]+)"', response.text)
            
            if version_match:
                github_version = version_match.group(1)
                local_version = self.config.build_version
                
                if github_version == local_version:
                    self.logger.log("UPDATER", "You are using the latest version.")
                    time.sleep(1)
                    return False
                else:
                    self.logger.log("UPDATER", f"Update available! Latest version: {github_version} - Your version: {local_version}")
                    time.sleep(1)
                    return True
            else:
                self.logger.log("UPDATER", "Failed to extract version from GitHub. Please check manually.")
                time.sleep(1)
                return False
        else:
            self.logger.log("UPDATER", "Failed to fetch updates from GitHub. Please check your internet connection.")
            time.sleep(1)
            return False