import discord
import commonbot.utils

def fetch_user(server, userid):
    return discord.utils.get(server.members, id=userid)

class UserLookup:
    def __init__(self):
        self.recent_bans = {}

    def add_ban(self, userid, username):
        self.recent_bans[userid] = username

    # Attempts to return a user ID
    def parse_id(self, message):
        content = commonbot.utils.strip_words(message.content, 1)
        try:
            # Simply verify by attempting to cast to an int. If it doesn't raise an error, return it
            # NOTE: This requires the ID to be first word, after the command
            checkID = content.split()[0]
            return int(checkID)
        except (IndexError, ValueError):
            return None

    def fetch_username(self, server, userid):
        username = None

        member = fetch_user(server, userid)
        if member != None:
            # If we found a member in the server, simply format the username
            username = f"{str(member)}"

        if username == None:
            # If user has recently left, use that username
            if userid in self.recent_bans:
                username = self.recent_bans[userid]

        return username
