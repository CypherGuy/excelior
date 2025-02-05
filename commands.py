# commands.py
import time


class CommandProcessor:
    def __init__(self):
        self.commands = {
            "/help": self.help_command,
            "/ping": self.ping_command,
            "/time": self.time_command,
            "/roles": self.roles_command,
            # Add more commands here
        }
        self.start_time = time.time()

    def process_command(self, message):
        """
        Parses and executes commands.
        """
        parts = message.strip().split(" ", 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command in self.commands:
            return self.commands[command](args)

    def help_command(self):
        """
        Returns a list of available commands.
        """
        command_list = "\n".join([
            "/ping - Test the bot's responsiveness",
            "/time - Show how long the bot has been running",
            "/roles - Get a link to the roles guide",
        ])
        return f"**Available Commands:**\n{command_list}"

    def ping_command(self):
        """
        Responds with 'Pong'.
        """
        return "Pong!"

    def pong_command(self):
        """
        Responds with 'Pong'.
        """
        return "Ping!"

    def time_command(self):
        """
        Shows how long the bot has been running.
        """
        uptime = time.time() - self.start_time
        minutes, seconds = divmod(int(uptime), 60)
        hours, minutes = divmod(minutes, 60)
        return f"I've been running for {hours}h {minutes}m {seconds}s."

    def roles_command(self):
        """
        Sends a link to the roles guide.
        """
        return "For a list of roles, visit: https://mafia.gg/guide/roles"
