import discord, commonbot.utils

class Debug:
    def __init__(self, owner, prefix, is_debug):
        self.debugging = False
        self.owner = owner
        self.prefix = prefix
        self.is_debug = is_debug

    def check_toggle(self, message):
        command = commonbot.utils.get_first_word(message.content).lower()
        return command == f"{self.prefix}debug"

    async def toggle_debug(self, message):
        if message.author.id == self.owner and not self.is_debug:
            self.debugging = not self.debugging
            enable_mes = "enabled" if self.debugging else "disabled"
            dbg_mes = f"Debugging {enable_mes}"
            await message.channel.send(dbg_mes)

    def is_debug_bot(self):
        return self.is_debug

    def should_ignore_message(self, message):
        if self.debugging and message.author.id == self.owner:
            # If debugging, the live bot should ignore the owner
            return True
        elif self.is_debug and message.author.id != self.owner:
            # If the debug bot, then ignore everyone else besides the owner
            return True
        else:
            return False
