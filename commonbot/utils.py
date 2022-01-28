import discord
from datetime import datetime

# Strips the prefix character from a string
def strip_prefix(m: str, prefix: str) -> str:
    return m[len(str(prefix)):]

# Strips num words from front of a sentence
def strip_words(m: str, num: int) -> str:
    to_remove = m.split()[0:num]
    size = 0
    for x in to_remove:
        size += len(x) + 1

    # This perserves whitespace
    return m[size:]

# Fetches the first word from a sentence
def get_first_word(m: str) -> str:
    try:
        return m.split()[0]
    except IndexError:
        return ""

# Input t is of the form: YYYY-MM-DD HH:MM:SS.SSSSSS
# Output is of the form YYYY-MM-DD
def format_time(t: datetime) -> str:
    date = str(t).split()[0]
    return date

# Checks if given user has one of the roles specified in config.json
def check_roles(user: discord.Member, valid_roles: list[int]) -> bool:
    for role in user.roles:
        if role.id in valid_roles:
            return True
    return False

# Since usernames can have spaces, first check if it's a username, otherwise just cut off first word as normal
def parse_message(message: str, username: str) -> str:
    m = " ".join(message.split()[1:])
    if m.startswith(username):
        return m[len(username)+1:]
    return strip_words(message, 2)

def get_time_delta(t1: datetime, t2: datetime) -> tuple[int, int, int]:
    # t1 should be larger than t2
    delta = t1 - t2
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return delta.days, hours, minutes

# Combines message content and attachment URLs together
def combine_message(mes: discord.Message) -> str:
    out = mes.content
    if mes.attachments != []:
        for item in mes.attachments:
            out += '\n' + item.url

    return out
