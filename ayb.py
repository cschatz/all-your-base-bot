import discord

# Bad practice! Needs to eventually
# move to somewhere else local
TOKEN = "OTQwNDgxODgyOTEzNjQwNTA4.YgICAg.uecQGHPZq1TU5TJUZ7xfE3cewg4"

client = discord.Client()


class QuoteFactory:
    def __init__(self, quotes):
        self.quotes = quotes
        self.index = -1

    def next(self):
        self.index = (self.index + 1) % len(self.quotes)
        return self.quotes[self.index]


memes = QuoteFactory([
    "Somebody set up us the bomb.",
    "Main screen turn on.",
    "All your base are belong to us.",
    "You have no chance to survive make your time.",
    "Move ZIG for great justice."
])

facts = QuoteFactory([
    "Dental floss has superb tensile strength.",
    "The square root of rope is string.",
    "Humans can survive underwater. But not for very long."
    "According to most advanced algorithms, the world's best name is Craig.",
    "This situation is hopeless."
    "Tungsten has the highest melting point of any metal."
    "Before the invention of scrambled eggs in 1912, the typical breakfast "
    "was either whole eggs still in the shell or scrambled rocks.",
    "In Greek myth, the craftsman Daedalus invented human flight so a group "
    "of Minotaurs would stop teasing him about it.",
])


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

# client.run(TOKEN)

f = Foo()
