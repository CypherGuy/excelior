# main.py

import asyncio
import os
from auth import Authenticator
from websocket_client import WebSocketClient


async def main():
    # Initialize Authenticator and authenticate
    authenticator = Authenticator()
    try:
        token, userid = await authenticator.authenticate()
    except Exception as e:
        print(f"Failed to authenticate: {e}")
        return

    # Initialize WebSocket Client

    room_id = input("Enter room ID or leave blank to make a default room: ")
    ws_client = WebSocketClient(
        token, userid, room_id, auth_token=os.getenv('AUTH_TOKEN'))

    # Connect and run the bot
    await ws_client.connect()

if __name__ == "__main__":
    asyncio.run(main())
