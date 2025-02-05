# helper_functions.py

import json


async def send_message(websocket, message):
    """
    Sends a chat message through the WebSocket.
    """
    chat_message = {
        "type": "chat",
        "message": message
    }
    await websocket.send(json.dumps(chat_message))
    print(f"Sent message: {message}")


def load_settings(file_path):
    """
    Loads settings from a JSON file.
    """
    import json
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_settings(file_path, settings):
    """
    Saves settings to a JSON file.
    """
    import json
    with open(file_path, 'w') as f:
        json.dump(settings, f, indent=4)
