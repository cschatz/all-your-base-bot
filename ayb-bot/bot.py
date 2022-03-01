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
        self.music_dir = parser.get("local", "music_directory")

    async def on_ready(self):
        """Set activity so users see 'listening to .base'"""
        print(f"Logged in as {self.user}")
        listening_activity = Activity(
            type=ActivityType.listening,
            name=".base"
        )
        await self.change_presence(activity=listening_activity)

    async def on_message(self, message):
        """Check any message posted, respond if it begins with .base"""
        if message.author == self.user:
            return
        if (request := message.content).startswith('.base'):
            tokens = request.split(" ")
            if tokens[0] != ".base":
                print(f"We ignored a possible request '{message.content}'")
            else:
                # Save most recent channel and author (sender) in instance vars
                self.channel = message.channel
                self.author = message.author
                if len(tokens) == 1:
                    self.show_help()
                else:
                    self.handle_request(message.author, tokens[1:])

    def run(self):
        """Start the bot"""
        super().run(self.token)

    def send_message(self, message):
        """Send any message on a given channel"""
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
        """Validate a music request, possibly initiating the playing of a
        particular file in a voice channel the sender has already joined"""
        voice = self.author.voice
        if not voice or not (voice_channel := voice.channel):
            self.send_message("You need to be in a voice channel first!")
        elif not args:
            self.send_message("You need to give me a file path!")
        else:
            # User may have typed a multi-word filename
            filename = " ".join(args)
            # Doing an initial check of the path because the FFmpegPCMAudio
            # constructor annoyingly won't raise an exception on invalid
            # path/file. Instead it spawns a subprocess and will send any error
            # straight to stderr.
            path = f"{self.music_dir}/{filename}"
            if not os.path.isfile(path):
                self.report_error(f"I'm sorry, I could not find {path}.")
            else:
                audio = FFmpegPCMAudio(
                    executable=self.ffmpg_app,
                    source=path
                )
                self.send_message(
                    f"Ok, I will try to play **{filename}** in **{voice_channel}**"
                )
                asyncio.create_task(self.play_music(voice_channel, audio))

    async def play_music(self, user_voice_channel, audio):
        """Start playing the given audio"""
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
