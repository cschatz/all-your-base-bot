import asyncio
from discord import Client, Activity, ActivityType, FFmpegPCMAudio
from configparser import ConfigParser
from quotation.collections import (
    FactQuotes,
    MemeQuotes,
)


class AllYourBASEBot(Client):
    def __init__(self, ini_file):
        super().__init__()
        self.channel = None
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
            if len(request) == 5:  # ".base" entered alone
                self.show_help()
            elif request[5] == " ":  # ".base [something]"
                self.handle_request(message.author, request[6:])
            else:
                print(f"Ignored possible request '{message.content}'")

    def run(self):
        super().run(self.token)

    def send_message(self, message):
        asyncio.create_task(self.channel.send(message))

    def handle_request(self, author, request):
        if not request:
            self.show_help()
        else:
            if request in ("fact", "meme"):
                quote_src = self.facts if request == "fact" else self.memes
                quote = quote_src.next()
                self.send_message(f"***{quote}***")
            elif request == "music":
                self.handle_music()
            else:
                self.show_help()

    def handle_music(self):
        voice = self.author.voice
        if not voice or not (voice_channel := voice.channel):
            self.send_message("You need to be in a voice channel first!")
        else:
            self.send_message(
                f"I see that you are **{voice_channel}** voice channel."
            )
            self.send_message("I will try to play music there.")
            # For now, a hardcoded path to an audio file
            filename = "/Users/cschatz/Desktop/gale.mp3"
            audio = FFmpegPCMAudio(
                executable=self.ffmpg_app,
                source=filename
            )
            asyncio.create_task(self.play_music(voice_channel, audio))

    async def play_music(self, voice_channel, audio):
        voice_client = await voice_channel.connect()
        voice_client.play(audio)

    def show_help(self):
        help_lines = [
            "Currently, I am mostly just an experiment.",
            "Commands available include...",
            "`.base fact`: request a fact",
            "`.base meme`: request a meme",
            "`.base music`: play some music"
        ]
        self.send_message("\n".join(help_lines))
