import re

class SteamAccount:

    @staticmethod
    def fetch_account_by_string(account):
        try:
            separator = ':' if ':' in account else '----'
            pattern = re.compile(f'(.*?){separator}', re.S)
            splitaccount = account.split('ssfn')
            info = pattern.findall(account)
            username, password, ssfn = info[0], info[1], splitaccount[1]
            return username, password, ssfn
        except:
            print('Incorrect account format. Expected format: username----password----ssfnXXXX or username:password:ssfnXXXX')
            exit()