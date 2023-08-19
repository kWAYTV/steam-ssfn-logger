import os, logging
from src.util.logger import Logger
from src.helper.config import Config
from src.handler.menu_manager import MenuManager
from src.helper.file_manager import FileManager

# Set title
if os.name == 'nt':
    os.system("title SSFN Logger Tool • Ready! • discord.gg/kws")

# Set logging system
logging.basicConfig(handlers=[logging.FileHandler('ssfntool.log', 'w+', 'utf-8')], level=logging.ERROR, format='%(asctime)s: %(message)s')

class Main():
    def __init__(self) -> None:
        self.logger = Logger()
        self.config = Config()
        self.file_manager = FileManager()
        self.menu_manager = MenuManager()

    def start(self):
        # Clean the screen, print the logo and start the logger
        self.logger.print_logo()
        self.logger.log("INFO", f"Welcome, {self.config.username}! Starting SSFN Logger Tool...")

        # Check if the files are there
        self.file_manager.check_input()

        # Display the menu
        self.menu_manager.display_main_menu()

if __name__ == "__main__":
    app = Main()
    app.start()