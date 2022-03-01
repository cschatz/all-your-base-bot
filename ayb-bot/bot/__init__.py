import discord
from configparser import ConfigParser

from quotation.collections import (
    FactQuotes,
    MemeQuotes,
)


class AllYourBASEBot(discord.Client):
    def __init__(self, ini_file):
        super().__init__()
        self.facts = FactQuotes()
        self.memes = MemeQuotes()
        parser = ConfigParser()
        parser.read(ini_file)
        self.token = parser.get("discord", "bot_token")

    def run(self):
        print("HERE")
        super().run(self.token)

    async def on_ready(self):
        print(f"We have logged in as {self.user}")
        listening_activity = discord.Activity(
            type=discord.ActivityType.listening,
            name=".base"
        )
        await self.change_presence(activity=listening_activity)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('.base'):
            if len(message.content) == 5:
                # ".base" entered alone
                await self._show_help(message.channel)
            elif message.content[5] == " ":
                # ".base [somethinng]"
                await self._respond(message.channel, message.content[6:])

    async def _respond(self, channel, query):
        if not query:
            await self._show_help(channel)
        else:
            if query == "fact":
                await channel.send("***" + self.facts.next() + "***")
            elif query == "meme":
                await channel.send("***" + self.memes.next() + "***")
            else:
                await self._show_help(channel)

    async def _show_help(self, channel):
        info = "Currently, I am just an experiment.\n"\
            "Commands include:\n"\
            "`.base fact` - request a fact\n"\
            "`.base meme` - request a meme"
        await channel.send(info)
