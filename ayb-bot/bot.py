import asyncio
import os
from discord import (
    Client,
    Activity,
    ActivityType,
    FFmpegPCMAudio,
    ClientException
)
from configparser import ConfigParser
from quotation.collections import (
    FactQuotes,
    MemeQuotes,
)


class AllYourBASEBot(Client):
    def __init__(self, ini_file):
        super().__init__()
        self.channel = None
        self.voice_channel = None
        self.author = None
        self.facts = FactQuotes()
        self.memes = MemeQuotes()
        parser = ConfigParser()
        parser.read(ini_file)
        self.token = parser.get("discord", "bot_token")
        self.ffmpg_app = parser.get("local", "ffmpeg_executable")

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        listening_activity = Activity(
            type=ActivityType.listening,
            name=".base"
        )
        await self.change_presence(activity=listening_activity)

    async def on_message(self, message):
        if message.author == self.user:
            return
        self.channel = message.channel
        self.author = message.author
        if (request := message.content).startswith('.base'):
            tokens = request.split(" ")
            if tokens[0] != ".base":
                print(f"We ignored a possible request '{message.content}'")
            elif len(tokens) == 1:
                self.show_help()
            else:
                self.handle_request(message.author, tokens[1:])

    def run(self):
        super().run(self.token)

    def send_message(self, message):
        asyncio.create_task(self.channel.send(message))

    def report_error(self, message):
        self.send_message(f"**ERROR: {message}**")

    def handle_request(self, author, request):
        command, *args = request
        if command in ("fact", "meme"):
            quote_src = self.facts if command == "fact" else self.memes
            quote = quote_src.next()
            self.send_message(f"***{quote}***")
        elif command == "music":
            self.handle_music(args)
        else:
            self.show_help()

    def handle_music(self, args):
        voice = self.author.voice
        if not voice or not (voice_channel := voice.channel):
            self.send_message("You need to be in a voice channel first!")
        elif not args:
            self.send_message("You need to give me a file path!")
        else:
            self.send_message(
                f"I see that you are **{voice_channel}** voice channel."
            )
            path = " ".join(args)
            self.send_message(
                f"I will now try to play music from local path '{path}'")
            # check path separately because the FFmpegPCMAudio constructor
            # otherwise does funky subprocess stuff that makes any error go
            # straight to stderr
            if not os.path.isfile(path):
                self.report_error(f"The path '{path}' is not valid.")
            else:
                audio = FFmpegPCMAudio(
                    executable=self.ffmpg_app,
                    source=path
                )
                asyncio.create_task(self.play_music(voice_channel, audio))

    async def play_music(self, user_voice_channel, audio):
        if not self.voice_clients:  # bot is not in a voice channel yet
            voice_client = await user_voice_channel.connect()
        else:
            if self.voice_clients[0].channel != user_voice_channel:
                await self.voice_clients[0].disconnect()
                voice_client = await user_voice_channel.connect()
            else:
                voice_client = self.voice_clients[0]
        try:
            voice_client.play(audio)
        except ClientException as e:
            self.report_error(e)

    def show_help(self):
        help_lines = [
            "Currently, I am mostly just an experiment.",
            "Commands available include...",
            "`.base fact`: request a fact",
            "`.base meme`: request a meme",
            "`.base music [path to local file]`: play some music"
        ]
        self.send_message("\n".join(help_lines))
