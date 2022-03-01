# AllYourBase Bot

This repo contains the source code for the AllYourBase bot.

It doesn't currently use any package management in a sensible way, sorry!

## Dependencies

(1) Python packages for Discord + PyNaCl
```
python3 -m pip install -U discord.py[voice]
```

(2) The Opus audio codec<br />
(Note this is a Mac-specific install command)
```
brew install opus
```

(3) The FFmpeg application -- download from https://www.ffmpeg.org/download.html.

## Configuration

Before running the bot, copy the `ayb-skeleton.ini` file into a new file named
`ayb.ini`. Fill in each entry with real values, including your Discord bot token
and the path to the FFmpeg executable you downloaded.

## Running the Bot

Launch the bot from within the root of the project directory with:
```
python3 ayb-bot
```
