import re
from typing import Optional

import discord

from commonbot.utils import strip_words

class UserLookup:
    def __init__(self):
        self.recent_bans = {}

    def add_ban(self, userid: int, username: str):
        self.recent_bans[userid] = username

    # Attempts to return a user ID
    def parse_id(self, message: discord.Message) -> Optional[int]:
        # Users can be mentioned one of three ways:
        # - By their ID
        # - By their username
        # - By pinging them

        user_id = self._check_id(message)

        if not user_id:
            user_id = self._check_username(message)

        if not user_id:
            user_id = self._check_mention(message)

        return user_id

    def _check_id(self, message: discord.Message) -> Optional[int]:
        content = strip_words(message.content, 1)

        try:
            # If ping is typed out by user using their ID, it doesn't count as a mention
            # Thus, try and match with regex
            check_ping = re.search(r"<@!?(\d+)>", content)
            if check_ping:
                return int(check_ping.group(1))

            # Simply verify by attempting to cast to an int. If it doesn't raise an error, return it
            # NOTE: This requires the ID to be first word, after the command
            check_id = content.split()[0]
            return int(check_id)
        except (IndexError, ValueError):
            return None

    def _check_username(self, message: discord.Message) -> Optional[int]:
        # Usernames can have spaces, so need to throw away the first word (the command),
        # and then everything after the discriminator
        test_username = strip_words(message.content, 1)

        try:
            # Some people *coughs* like to put a '@' at beginning of the username.
            # Remove the '@' if it exists at the front of the message
            if test_username[0] == "@":
                test_username = test_username[1:]

            # Parse out the actual username
            user = test_username.split("#")
            discriminator = user[1].split()[0]
            user_found = discord.utils.get(message.guild.members, name=user[0], discriminator=discriminator)
            if user_found:
                return user_found.id

            # If not found in server, check if they're in the recently banned dict
            fullname = f"{user[0]}#{discriminator}"
            if fullname in list(self.recent_bans.values()):
                rev_bans = {v: k for k, v in self.recent_bans.items()}
                return rev_bans[fullname]
            return None
        except IndexError:
            return None

    def _check_mention(self, message: discord.Message) -> Optional[int]:
        try:
            return message.mentions[0].id
        except IndexError:
            return None

    def fetch_username(self, client: discord.Client, userid: int) -> Optional[str]:
        username = None

        member = client.get_user(userid)
        if member:
            # If we found a member in the server, simply format the username
            username = f"{str(member)}"

        if not username:
            # If user has recently left, use that username
            if userid in self.recent_bans:
                username = self.recent_bans[userid]

        return username
