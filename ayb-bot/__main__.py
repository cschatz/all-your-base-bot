#!/usr/bin/env python3

import discord
from quotations import FactQuotes, MemeQuotes

# Bad practice! Needs to eventually
# move to somewhere else local
TOKEN = "OTQwNDgxODgyOTEzNjQwNTA4.YgICAg.uecQGHPZq1TU5TJUZ7xfE3cewg4"

client = discord.Client()

facts = FactQuotes()
memes = MemeQuotes()


async def show_help(channel):
    info = "Currently, I am barely implemented.\n"\
        "Commands include:\n"\
        "`.base fact` - request a fact\n"\
        "`.base meme` - request a meme"
    await channel.send(info)


async def respond(channel, query):
    if not query:
        await show_help(channel)
    else:
        if query == "fact":
            await channel.send("***" + facts.next() + "***")
        elif query == "meme":
            await channel.send("***" + memes.next() + "***")
        else:
            await show_help(channel)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    listening_activity = discord.Activity(
        type=discord.ActivityType.listening,
        name=".base"
    )
    await client.change_presence(activity=listening_activity)


@client.event
async def on_message(message):
    global index

    if message.author == client.user:
        return

    if message.content.startswith('.base'):
        if len(message.content) == 5:
            # ".base" entered alone
            await show_help(message.channel)
        elif message.content[5] == " ":
            # ".base [somethinng]"
            await respond(message.channel, message.content[6:])

client.run(TOKEN)
