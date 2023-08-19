import os, re, requests

class SSFNHandler:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        }

    def download(self, ssfn, steam_path):
        removed_files = 0
        url = f'https://ssfnbox.com/download/ssfn{ssfn}'
        print("Requesting SSFN file...")

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        body = response.text

        sec_value = re.search(r'window\.location\.assign\("/download/ssfn\d+\?sec=(\w+?)"\)', body)
        if not sec_value:
            print("Failed to extract sec value, is your ssfn valid?")
            exit()

        final_url = f"https://ssfnbox.com/download/ssfn{ssfn}?sec={sec_value.group(1)}"
        response = requests.get(final_url, headers=self.headers)
        response.raise_for_status()

        for file in os.listdir(steam_path):
            if file.startswith(f'ssfn'):
                os.remove(os.path.join(steam_path, file))
                removed_files += 1
        
        if removed_files > 0:
            print(f"Removed {removed_files} old ssfn files.")

        filename = os.path.join(steam_path, f'ssfn{ssfn}')
        with open(filename, 'wb') as f:
            f.write(response.content)