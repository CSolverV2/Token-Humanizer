import random
import threading
from time import sleep
import os
from os.path import isfile, join
from colorama import Fore, init
import tls_client
import base64
import json

init(autoreset=True)


class EditMe:
    def __init__(self):
        self.useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        self.session = tls_client.Session(random_tls_extension_order=True, client_identifier="chrome_130")
        self.build_number = self._get_build_number()
        self.usednames = []
        self.totalnames = len(open('./data/usernames.txt', encoding='utf-8').read().splitlines())

    def _get_build_number(self):
        try:
            response = self.session.get("https://api.sockets.lol/discord/build")
            return int(response.json()['build'])
        except:
            return 345368

    def _get_super_properties(self):
        return base64.b64encode(json.dumps({
            "os": "Windows",
            "browser": "Chrome",
            "browser_user_agent": self.useragent,
            "browser_version": "130.0.0.0",
            "os_version": "10",
            "release_channel": "stable",
            "client_build_number": self.build_number
        }).encode()).decode()

    def _cookies(self):
        while True:
            try:
                response = self.session.get("https://discord.com")
                return (
                    response.cookies.get('__cfruid'),
                    response.cookies.get('__dcfduid'),
                    response.cookies.get('__sdcfduid'),
                    response.cookies.get("_cfuvid"),
                    response.cookies.get("cf_clearance")
                )
            except:
                sleep(1)

    def _get_username(self):
        with open('./data/usernames.txt', encoding='utf-8') as file:
            usernames = file.read().splitlines()
        available_usernames = [u for u in usernames if u not in self.usednames]
        if not available_usernames:
            self.usednames.clear()
            available_usernames = usernames
        username = random.choice(available_usernames)
        self.usednames.append(username)
        return username

    def _get_avatar(self):
        picture = [f for f in os.listdir("./data/pfp/") if isfile(join("./data/pfp/", f))]
        random_picture = random.choice(picture)
        return base64.b64encode(open(f'./data/pfp/{random_picture}', 'rb').read()).decode()

    def _get_bio(self):
        bios = open('./data/bios.txt', encoding='utf-8').read().splitlines()
        return random.choice(bios) if bios else 'discord.gg/csolve | t.me/csolver'

    def _update(self, token, proxy, endpoint, data, success_msg, fail_msg):
        try:
            self.session.proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            __cfruid, __dcfduid, __sdcfduid, _cfuvid, cf_clearance = self._cookies()
            self.session.headers = {
                'accept': '*/*',
                'accept-language': 'en,de;q=0.9',
                'authorization': token,
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                'cookie': f'__dcfduid={__dcfduid}; __sdcfduid={__sdcfduid}; __cfruid={__cfruid}; _cfuvid={_cfuvid}; cf_clearance={cf_clearance}',
                'dnt': '1',
                'origin': 'https://discord.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://discord.com/channels/@me',
                'sec-ch-ua': '"Chromium";v="130", "Avast Secure Browser";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Avast/130.0.0.0',
                'x-debug-options': 'bugReporterEnabled',
                'x-discord-locale': 'en-US',
                'x-discord-timezone': 'America/Los_Angeles',
                'x-super-properties': self._get_super_properties(),
            }
            response = self.session.patch(endpoint, json=data)
            if response.status_code in [200, 204]:
                print(Fore.GREEN + success_msg)
            else:
                print(Fore.RED + fail_msg)
        except:
            print(Fore.RED + fail_msg)

    def checkme(self, token):
        try:
            self.session.headers = {'authorization': token, 'user-agent': self.useragent}
            response = self.session.get("https://discord.com/api/v9/users/@me")
            return response.status_code == 200
        except:
            return False

    def humanize(self, token, proxy):
        print(Fore.YELLOW + f"Humanizing: {token[:30]}****")
        self._update(token, proxy, "https://discord.com/api/v9/users/@me",
                     {"avatar": f"data:image/jpeg;base64,{self._get_avatar()}"},
                     "Profile picture updated.", "Failed to update profile picture.")
        self._update(token, proxy, "https://discord.com/api/v9/users/@me/profile",
                     {"bio": self._get_bio()},
                     "Bio updated.", "Failed to update bio.")
        self._update(token, proxy, "https://discord.com/api/v9/users/@me",
                     {"global_name": self._get_username()},
                     "Username updated.", "Failed to update username.")
        self._update(token, proxy, "https://discord.com/api/v9/users/@me/profile",
                     {"pronouns": random.choice(["he/him", "she/her", "they/them"])},
                     "Pronouns updated.", "Failed to update pronouns.")
        print(Fore.CYAN + f"Successfully humanized: {token[:30]}****\n")

    def start(self, proxies):
        tokens = [line.strip().split(':')[-1] if ':' in line else line.strip() for line in open('./tokens.txt', 'r') if line.strip()]

        def worker(tokenz):
            for token in tokenz:
                proxy = random.choice(proxies)
                if self.checkme(token):
                    print(Fore.GREEN + f"Valid Token: {token[:30]}****")
                    self.humanize(token, proxy)
                else:
                    print(Fore.RED + f"Invalid Token: {token[:30]}****")

        size = len(tokens) // 5 + (len(tokens) % 5 > 0)
        chunks = [tokens[i:i + size] for i in range(0, len(tokens), size)]

        threads = []
        for chunk in chunks[:5]:  
            thread = threading.Thread(target=worker, args=(chunk,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    os.system("cls")
    print(Fore.CYAN + """
        Discord Humanizer
    ------------------------
    [1] Humanize Tokens
    [2] Quit
    """)
    choice = int(input("Choice >>> "))
    if choice == 1:
        with open("./proxies.txt", 'r', encoding='utf-8') as file:
            proxies = [line.strip() for line in file.readlines()]
        humanizer = EditMe()
        humanizer.start(proxies)
    else:
        quit()
