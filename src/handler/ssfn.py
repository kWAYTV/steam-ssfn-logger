import os, re, requests
from src.util.logger import Logger

class SSFNHandler:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        }
        self.logger = Logger()

    def download_ssfnbox(self, ssfn, steam_path):
        removed_files, attempts = 0, 0
        url = f'https://ssfnbox.com/download/ssfn{ssfn}'
        self.logger.log("INFO", "Requesting SSFN file...")

        response = requests.get(url, headers=self.headers)
        body = response.text

        sec_value = re.search(r'window\.location\.assign\("/download/ssfn\d+\?sec=(\w+?)"\)', body)

        while not sec_value and attempts < 5:
            attempts += 1
            self.logger.log("INFO", f"Failed to extract sec value, retrying... ({attempts}/5)")
            response = requests.get(url, headers=self.headers)
            body = response.text
            sec_value = re.search(r'window\.location\.assign\("/download/ssfn\d+\?sec=(\w+?)"\)', body)

        if not sec_value:
            self.logger.log("ERROR", "Failed to extract sec value.")
            return exit()

        final_url = f"https://ssfnbox.com/download/ssfn{ssfn}?sec={sec_value.group(1)}"
        response = requests.get(final_url, headers=self.headers)

        for file in os.listdir(steam_path):
            if file.startswith(f'ssfn'):
                os.remove(os.path.join(steam_path, file))
                removed_files += 1

        if removed_files > 0:
            self.logger.log("INFO", f"Removed {removed_files} old ssfn files.")

        filename = os.path.join(steam_path, f'ssfn{ssfn}')
        with open(filename, 'wb') as f:
            f.write(response.content)

    def download_server(self, ssfn, steam_path):
        url = f"tool.ctrl000.cc:66/ssfn/ssfn{ssfn}"
        self.logger.log("INFO", "Requesting SSFN file...")

        response = requests.get(url, headers=self.headers)

        for file in os.listdir(steam_path):
            if file.startswith(f'ssfn'):
                os.remove(os.path.join(steam_path, file))
                removed_files += 1

        if removed_files > 0:
            self.logger.log("INFO", f"Removed {removed_files} old ssfn files.")

        filename = os.path.join(steam_path, f'ssfn{ssfn}')
        with open(filename, 'wb') as f:
            f.write(response.content)