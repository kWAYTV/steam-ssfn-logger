import os, re, requests

class SSFNHandler:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        }

    def download(self, ssfn, steam_path):
        url = f'https://ssfnbox.com/download/ssfn{ssfn}'
        print("Requesting SSFN file...")

        response = requests.get(url, headers=self.headers)
        body = response.text

        sec_value = re.search(r'window\.location\.assign\("/download/ssfn\d+\?sec=(\w+?)"\)', body)
        if not sec_value:
            print("Failed to extract sec value, is your ssfn valid?")
            exit()

        final_url = f"https://ssfnbox.com/download/ssfn{ssfn}?sec={sec_value.group(1)}"
        response = requests.get(final_url, headers=self.headers)

        for file in os.listdir(steam_path):
            if file.startswith(f'ssfn{ssfn}'):
                os.remove(os.path.join(steam_path, file))
                print("Removed old SSFN file")

        filename = os.path.join(steam_path, f'ssfn{ssfn}')
        with open(filename, 'wb') as f:
            f.write(response.content)