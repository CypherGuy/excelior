# Excelior

Excelior is a [**mafia.gg bot**](https://www.mafia.gg) designed for me to experiment with WebSocket communications and authentication methods. This bot connects to mafia.gg and automatically joins a room, allowing interaction with the game through user-ran commands in the ingame chat. I initially adopted a Selenium-based approach but due to the open window and slow bot response times, I decided to learn more about WebSockets and how they work.

## Features

- 🔌 **WebSocket Client** – Handles real-time communication with Mafia.gg via websockets
- 🔑 **Authentication System** – Manages user authentication for secure connections
- 📜 **Command Scalability** – Easily scale up commands as you want
- 🛠 **Modular Structure** – Designed for easy expansion and customisation

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/CypherGuy/excelior.git
cd excelior
pip install -r requirements.txt
```

## Usage

Modify settings.json to include your authentication details and room ID:

```json
{
    "token": "your_token_here",
    "userid": "your_userid_here",
    "room_id": "optional_room_id"
}
```

Add a .env file, and put in your username, password and auth token

```env
USERNAME = 'username'
PASSWORD = 'password'
AUTH_TOKEN = 'authtoken'
```

then run the bot
```
python main.py
```

In the terminal you can give it a URL to connect to a specific room URL, or it will find the first one available and join it.

## File Structure

```
excelior/
│── auth.py               # Handles authentication
│── commands.py           # Defines bot commands
│── helper_functions.py   # Utility functions
│── main.py               # Main bot logic
│── websocket_client.py   # WebSocket client implementation
│── settings.json         # Configuration file
│── requirements.txt      # Dependencies
│── .gitignore            # Git ignore rules
```

I would also highly recommend you put in a .env file for you to put your bot's username, password and auth token.

## Contributions
Contributions are welcome! If you'd like to add features or improve the bot:

- Fork the repo.
- Create a new branch (git checkout -b feature-name).
- Commit your changes (git commit -m "Add new feature").
- Push to the branch (git push origin feature-name).
- Open a pull request.

## License
This project is licensed under the MIT License.

## Contact
For questions or issues, open an issue on GitHub.
