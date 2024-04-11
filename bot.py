#Foreign imports
import discord
import json
import os

#Local imports
import message


def run_bot():
    #Get token from credentials.json file
    file_path = os.path.join(os.path.dirname(__file__), './credentials.json')
    discord_token = json.load(open(file_path, 'r'))["token"]

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