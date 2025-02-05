# auth.py
import os
from dotenv import load_dotenv
from aiohttp import ClientSession

load_dotenv()


class Authenticator:
    def __init__(self):
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.token = None
        self.userid = None
        self.session = None  # aiohttp session

    async def authenticate(self):
        """
        Authenticates with Mafia.gg and retrieves session token and user ID.
        """
        login_url = "https://mafia.gg/api/user-session"
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0",
            "Accept": "application/json, text/*",
        }
        payload = {
            "login": self.username,
            "password": self.password
        }

        async with ClientSession() as session:
            async with session.post(login_url, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Authentication failed with status code {resp.status}")
                data = await resp.json()
                self.token = resp.cookies.get("userSessionToken").value
                self.userid = data.get("id")
                print(f"Authenticated successfully. User ID: {self.userid}")
                return self.token, self.userid
