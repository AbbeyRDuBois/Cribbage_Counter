#Foreign imports
import discord

#Local imports
import message
import credentials

def run_bot():
    #Get token from credentials.json file
    discord_token = credentials.load_from_file("credentials.json")

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

    try:
        client.run(discord_token)
    except Exception as e:
        print("ERROR: " + str(e))