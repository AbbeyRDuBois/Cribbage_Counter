#Foreign imports
import discord
import json

#Local imports
import message


def run_bot():
    #Get token from credentials.json file

    # Try to open the credentials file, if it doesn't exist, create it.
    try:
        credentials_file = open('credentials.json', 'r')
    except FileNotFoundError:
        print("credentials.json not found. Creating file...")
        credentials_file = open('credentials.json', 'w')
        credentials_file.write('{\n\t"token": "YOUR_TOKEN' + '\n}')
        return

    discord_token = json.load(credentials_file)["token"]

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