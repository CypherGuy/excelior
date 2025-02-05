# websocket_client.py

# I plan to use asyncio in the future
import json
import websockets
from commands import CommandProcessor
from helper_functions import load_settings, save_settings, send_message
import os


class WebSocketClient:
    def __init__(self, token, userid, room_id=None, auth_token=None):
        self.token = token
        self.userid = userid
        self.room_id = room_id
        self.auth = auth_token
        self.websocket = None
        self.command_processor = CommandProcessor()
        self.settings = load_settings("settings.json")

    async def get_room_auth(self):
        """
        Retrieves room authentication details. If room_id is None, creates a new room.
        """
        import aiohttp

        async with aiohttp.ClientSession() as session:
            if self.room_id:
                # Join existing room
                room_url = f"https://mafia.gg/api/rooms/{self.room_id}"
                async with session.get(room_url, headers={"Cookie": f"userSessionToken={self.token}"}) as resp:
                    if resp.status != 200:
                        raise Exception(
                            f"Failed to retrieve room info: {resp.status}")
                    data = await resp.json()
            else:
                # Create a new room
                create_room_url = "https://mafia.gg/api/rooms/"
                payload = {
                    "name": self.settings.get("room_name", "Default Room"),
                    "unlisted": False
                }
                async with session.post(create_room_url, json=payload, headers={"Cookie": f"userSessionToken={self.token}"}) as resp:
                    if resp.status != 200:
                        raise Exception(
                            f"Failed to create room: {resp.status}")
                    data = await resp.json()
                    self.room_id = data.get("id")
                    print(f"""Created and joined new room with ID: {
                          self.room_id}""")

            self.auth = data.get("auth")
            print(f"Room Auth Token: {self.auth}")

    async def connect(self):
        """
        Establishes the WebSocket connection and starts listening for messages.
        """
        await self.get_room_auth()
        uri = "wss://mafia.gg:443/engine"
        async with websockets.connect(uri) as websocket:
            self.websocket = websocket
            await self.handshake()
            await self.send_initial_messages()
            await self.listen()

    async def handshake(self):
        """
        Performs the client handshake by sending necessary authentication details.
        """
        handshake_message = {
            "type": "clientHandshake",
            "userId": self.userid,
            "roomId": self.room_id,
            "auth": self.auth
        }
        await self.websocket.send(json.dumps(handshake_message))
        print("Handshake sent.")

    async def send_initial_messages(self):
        """
        Sends presence and introductory chat message.
        """
        presence_message = {"type": "presence", "isPlayer": False}
        await self.websocket.send(json.dumps(presence_message))
        print("Initial messages sent.")

    async def listen(self):
        """
        Listens for incoming WebSocket messages and processes them.
        """
        async for message in self.websocket:
            data = json.loads(message)
            await self.handle_message(data)

    async def handle_message(self, data):
        """
        Processes incoming messages based on their type.
        """
        msg_type = data.get("type")
        message = data.get("message", "")

        # Check if the system message indicates a new game
        print(message)
        if "The host has started another game!" in message:
            await self.process_new_game_message(message)
        elif msg_type == "chat":
            await self.handle_chat(data)
        elif msg_type == "system":
            await self.handle_system(data)

    async def handle_chat(self, data):
        """
        Handles incoming chat messages.
        """
        message = data.get("message", "")
        sender = data.get("from", {}).get("model")
        user_id = data.get("from", {}).get("userId")

        print(sender, user_id, message)

        if sender == "user":
            print(f"User {user_id} says: {message}")
            print("----------------------------")

            if message.startswith("/") and user_id == 490655:
                response = self.command_processor.process_command(message)
                if response:
                    await send_message(self.websocket, response)

    async def handle_system(self, data):
        """
        Handles system messages.
        """
        message = data.get("message", "")
        print(f"System message: {message}")

    async def process_new_game_message(self, message):
        """
        Extracts the new game link from the message and joins the room.
        """
        # Find the link in the message using string manipulation
        start_index = message.find('href="') + len('href="')
        end_index = message.find('"', start_index)
        new_game_url = message[start_index:end_index]

        # Print the new game URL
        print(f"A new game has been hosted! Joining: {new_game_url}")

        # Join the new game using the extracted URL
        await self.join_new_game(new_game_url)

    async def join_new_game(self, new_game_url):
        """
        Joins a new game room using the provided URL.
        """
        # Extract the room ID from the URL
        # Assuming the room ID is the last part of the URL
        room_id = new_game_url.split("/")[-1]
        self.room_id = room_id

        # Use the previously used auth token
        self.auth = os.getenv('AUTH_TOKEN')  # Or fetch it as needed

        await self.connect()  # Reconnect to the new game
