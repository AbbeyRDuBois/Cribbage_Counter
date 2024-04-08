#Foreign imports
import discord
import json

#Local imports
import message


def run_bot():
    #Get token from credentials.json file
    discord_token = json.load(open('credentials.json', 'r'))["token"]

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(client.user.name + ' is running.')

    @client.event
    async def on_message(msg):
        if msg.author == client.user:
            return
        
        await message.process_message(msg)

    client.run(discord_token)