import discord, re
from commonbot.utils import strip_words
from typing import Optional

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
            checkPing = re.search(r"<@!?(\d+)>", content)
            if checkPing:
                return int(checkPing.group(1))

            # Simply verify by attempting to cast to an int. If it doesn't raise an error, return it
            # NOTE: This requires the ID to be first word, after the command
            checkID = content.split()[0]
            return int(checkID)
        except (IndexError, ValueError):
            return None

    def _check_username(self, message: discord.Message) -> Optional[int]:
        # Usernames can have spaces, so need to throw away the first word (the command),
        # and then everything after the discriminator
        testUsername = strip_words(message.content, 1)

        try:
            # Some people *coughs* like to put a '@' at beginning of the username.
            # Remove the '@' if it exists at the front of the message
            if testUsername[0] == "@":
                testUsername = testUsername[1:]

            # Parse out the actual username
            user = testUsername.split("#")
            discriminator = user[1].split()[0]
            userFound = discord.utils.get(message.guild.members, name=user[0], discriminator=discriminator)
            if userFound:
                return userFound.id

            # If not found in server, check if they're in the recently banned dict
            fullname = f"{user[0]}#{discriminator}"
            if fullname in list(self.recent_bans.values()):
                revBans = {v: k for k, v in self.recent_bans.items()}
                return revBans[fullname]

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
