#!/usr/bin/env python3
# Decode By Error x Ethan.
try:
    import os, sys, requests, re, json, time, secrets
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    from fake_useragent import UserAgent
    from faker import Faker
    from rich import print as printf
    from rich.console import Console
    from rich.panel import Panel
    from requests.exceptions import RequestException
except ModuleNotFoundError:
    print("Error: Module not found. Please try again after installing the required modules.")
    sys.exit(1)

SUCCESS, FAILED, TIMES = [], [], {
    "SECONDS": 0
}

def BANNER() -> None:
    printf(
        Panel(r"""[bold red]    _______ _ _    ____                  _   _      
   |__   __(_) |  |  _ \                | | | |     
      | |   _| | _| |_) | ___   ___  ___| |_| |     
      | |  | | |/ /  _ < / _ \ / _ \/ __| __| |     
      | |  | |   <| |_) | (_) | (_) \__ \ |_| |____ 
[bold white]      |_|  |_|_|\_\____/ \___/ \___/|___/\__|______|
          [underline red]Free TikTok Followers - by Rozhak""", width=59, style="bold bright_black")
    )
    return None

def DELAY(total_seconds: int, tiktok_username: str) -> None:
    for sleep in range(int(total_seconds), 0, -1):
        time.sleep(1.0)
        printf(f"[bold bright_black]   ──>[bold green] @{str(tiktok_username).upper()}[bold white]/[bold yellow]{sleep}[bold white] SUCCESS:-[bold green]{len(SUCCESS)}[bold white] FAILED:-[bold red]{len(FAILED)}    ", end='\r')
    return None

class SUBMIT:

    def __init__(self) -> None:
        self.BASE_URL = "https://www.folloza.com"
        self.SESSION = requests.Session()

    def VISIT_SITE(self, tiktok_username: str, emails: str) -> None:
        self.SESSION.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.folloza.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': f'{UserAgent.random}'
        }
        response = self.SESSION.get(f"{self.BASE_URL}/free-tiktok-followers", allow_redirects=True)

        self.FOLLOWERS(tiktok_username, emails)

    def FOLLOWERS(self, tiktok_username: str, emails: str) -> bool:
        boundary = '----WebKitFormBoundary' + secrets.token_hex(16)

        data = MultipartEncoder(fields={
            'service_type': 'tiktok_free_followers',
            'email': f'{emails}',
            'channel_url': f'https://www.tiktok.com/@{tiktok_username}',
            'service_type': 'tiktok_free_followers',
        }, boundary=boundary)

        self.SESSION.headers.update(
            {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://www.folloza.com/free-tiktok-followers',
                'Sec-Fetch-Mode': 'cors',
                'Accept': '*/*',
                'Origin': 'https://www.folloza.com',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Length': '0',
            }
        )

        response = self.SESSION.post('https://www.folloza.com/process.php', data=data, allow_redirects=False)
        if '"verification_token":"' in response.text:
            verification_token = json.loads(response.text)['verification_token']

            self.SESSION.headers.pop('Content-Length')
            self.SESSION.headers.pop('Origin')
            self.SESSION.headers.pop('Content-Type')
            self.SESSION.headers.update(
                {
                    'Referer': f'https://www.folloza.com/free-tiktok-followers?token={verification_token}'
                }
            )
            response = self.SESSION.get(f'https://www.folloza.com/verify_activation.php?token={verification_token}', allow_redirects=True)
            if '"success":true' in response.text:
                printf(
                    Panel(f"""[bold white]Status:[bold green] Successfully sent followers!
[bold white]Link:[bold red] https://www.tiktok.com/@{tiktok_username}
[bold white]Followers:[bold yellow] +15""", width=59, style="bold bright_black", title="[bold bright_black]>> [Success] <<")
                )
                SUCCESS.append(f"{response.status_code}|{tiktok_username}|{emails}")
                return True
            else:
                printf(f"[bold bright_black]   ──>[bold red] FOLLOWERS NOT SUCCESSFULLY SENT!     ", end='\r')
                time.sleep(2.5)
                FAILED.append(f"{response.status_code}|{tiktok_username}|{emails}")
                return False
        elif 'You can only activate' in response.text:
            times_match = re.search(r'(\d{2}):(\d{2}):(\d{2})', response.text)
            if times_match:
                hours, minutes, seconds = map(int, times_match.groups())
                total_seconds = hours * 3600 + minutes * 60 + seconds
            else:
                total_seconds = 86400

            printf(f"[bold bright_black]   ──>[bold yellow] PLEASE WAIT {total_seconds} SECONDS!     ", end='\r')
            time.sleep(2.5)

            TIMES['SECONDS'] = total_seconds

            return False
        else:
            printf(f"[bold bright_black]   ──>[bold red] CANNOT FIND VERIFICATION TOKEN!     ", end='\r')
            time.sleep(2.5)
            return False

def MAIN() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    BANNER()
    printf(
        Panel(f"[bold white]Please enter your TikTok username and ensure your accou\nnt is not in private mode. You can\nuse '[bold green],[bold white]' as a separator to enter different usernames!", width=59, style="bold bright_black", title="[bold bright_black]>> [Tiktok Username] <<", subtitle="[bold bright_black]╭───────", subtitle_align="left")
    )
    username_list = Console().input("[bold bright_black]   ╰─> ").replace('@', '').strip().split(',')
    if len(username_list) > 0:
        printf(
            Panel(f"[bold white]You can use[bold yellow] CTRL + C[bold white] if you get stuck and[bold red] CTRL + Z[bold white] if you want to stop. *[bold red]Remember to use\na proxy for different usernames to avoid spam[bold white]!", width=59, style="bold bright_black", title="[bold bright_black]>> [Cannot be Empty] <<")
        )
        while True:
            try:
                for tiktok_username in username_list:
                    try:
                        SUBMIT().VISIT_SITE(tiktok_username, Faker().email(domain="gmail.com"))
                    except RequestException:
                        printf(f"[bold bright_black]   ──>[bold yellow] YOUR CONNECTION IS HAVING A PROBLEM!    ", end='\r')
                        time.sleep(10.0)
                        continue
                if TIMES['SECONDS'] > 0:
                    DELAY(total_seconds=int(TIMES['SECONDS']), tiktok_username=tiktok_username)
                TIMES['SECONDS'] = 0
            except Exception as e:
                printf(f"[bold bright_black]   ──>[bold red] {str(e).upper()}!", end='\r')
                time.sleep(5.0)
                continue
            except KeyboardInterrupt:
                printf(f"                                              ", end='\r')
                time.sleep(2.5)
                continue
    else:
        printf(
            Panel(f"[bold red]Sorry, you must enter at least one TikTok username. Please try again!", width=59, style="bold bright_black", title="[bold bright_black]>> [Cannot be Empty] <<")
        )
        sys.exit(1)

if __name__ == "__main__":
    try:
        if os.path.exists("Penyimpanan/Subscribe.json") == False:
            os.system(f"xdg-open {json.loads(requests.get('https://raw.githubusercontent.com/RozhakLabs/TikBoostLite/main/Penyimpanan/Youtube.json').text)['Link']}")
            with open('Penyimpanan/Subscribe.json', 'w') as w:
                w.write(json.dumps(
                    {
                        "Status": True
                    }, indent=4
                ))
            time.sleep(2.5)
        MAIN()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        printf(
            Panel(f"[bold red]{str(e).capitalize()}!", width=59, style="bold bright_black", title="[bold bright_black]>> [Error] <<")
        )
        sys.exit(1)
