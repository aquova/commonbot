from datetime import datetime
import discord

CHAR_LIMIT = 2000

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

# Input t is of the form: YYYY-MM-DD HH:MM:SS.SSSSSS
# Output is of the form YYYY-MM-DD
def format_time(time: datetime) -> str:
    date = str(time).split()[0]
    return date

# Checks if given user has one of the roles specified in config.json
def check_roles(user: discord.Member, valid_roles: list[int]) -> bool:
    for role in valid_roles:
        if user.get_role(role):
            return True
    return False

# Since usernames can have spaces, first check if it's a username, otherwise just cut off first word as normal
def parse_message(message: str, username: str) -> str:
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

async def send_message(message: str, channel: discord.TextChannel) -> discord.Message:
    mes_list = message.split('\n')
    first = None
    mes = mes_list[0]
    for line in mes_list[1:]:
        # Discord treats escape \ characters as two characters, while Python len() counts them as one.
        if len(mes.encode('unicode-escape')) > CHAR_LIMIT:
            first = mes[:CHAR_LIMIT]
            second = mes[CHAR_LIMIT:]
            sent = await channel.send(first)
            await channel.send(second)
            mes = ""
            if not first:
                first = sent

        next_string = f"{mes}\n{line}"

        if len(next_string.encode('unicode-escape')) < CHAR_LIMIT:
            mes = next_string
        else:
            sent = await channel.send(mes)
            if not first:
                first = sent
            mes = line
    if mes != "":
        sent = await channel.send(mes)
        if not first:
            first = sent
    return first
