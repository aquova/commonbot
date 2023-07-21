from datetime import datetime
from textwrap import wrap

import discord

CHAR_LIMIT = 1990 # The actual limit is 2000, but we'll be conservative

# Strips the prefix character from a string
def strip_prefix(txt: str, prefix: str) -> str:
    return txt[len(str(prefix)):]

# Strips num words from front of a sentence
def strip_words(txt: str, num: int) -> str:
    to_remove = txt.split()[0:num]
    size = 0
    for char in to_remove:
        size += len(char) + 1

    # This perserves whitespace
    return txt[size:]

# Fetches the first word from a sentence
def get_first_word(txt: str) -> str:
    try:
        return txt.split()[0]
    except IndexError:
        return ""

# Output is of the form YYYY-MM-DD
def format_time(time: datetime) -> str:
    date = str(time).split()[0]
    return date

# Checks if given user has one of the roles specified in config.json
def check_roles(user: discord.Member | discord.User, valid_roles: list[int]) -> bool:
    if isinstance(user, discord.User):
        return False
    for role in valid_roles:
        if user.get_role(role):
            return True
    return False

# Removes a user mention from a message
def parse_message(message: str, username: str, username_in_message: bool = True) -> str:
    # If the username isn't in the message, just strip the command from it
    if not username_in_message:
        return strip_words(message, 1)

    # Otherwise strip the command and username
    # Since usernames can have spaces, first check if it's a username, otherwise just cut off first word as normal
    txt = " ".join(message.split()[1:])
    if txt.startswith(username):
        return txt[len(username)+1:]
    return strip_words(message, 2)

# Gets the days, hours, minutes, seconds from the delta of two times
def get_time_delta(time1: datetime, time2: datetime) -> tuple[int, int, int, int]:
    # t1 should be larger than t2
    delta = time1 - time2
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return delta.days, hours, minutes, seconds

# Combines message content, attachment URLs, and stickers together
def combine_message(mes: discord.Message) -> str:
    out = mes.content
    for item in mes.attachments:
        out += '\n' + item.url

    for sticker in mes.stickers:
        out += '\n' + sticker.url

    return out

async def send_message(message: str, channel: discord.TextChannel | discord.Thread) -> discord.Message | None:
    messages = message.split('\n')
    to_send = [messages[0]]
    for msg in messages[1:]:
        if len(msg) >= CHAR_LIMIT:
            to_send += wrap(msg, width=CHAR_LIMIT)
        elif len(msg) + len(to_send[-1]) < CHAR_LIMIT:
            to_send[-1] += f"\n{msg}"
        else:
            to_send.append(msg)

    first_id = None
    for msg in to_send:
        if len(msg) > 0:
            mid = await channel.send(msg)
            first_id = mid if first_id is None else first_id
    return first_id

