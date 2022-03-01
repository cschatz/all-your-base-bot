from bot import AllYourBASEBot
import sys

# for logging
sys.stdout.flush()

client = AllYourBASEBot("ayb.ini")
client.run()
