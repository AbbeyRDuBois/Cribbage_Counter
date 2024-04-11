#Foreign imports
import discord

#Local imports
import message
import credentials
import format

def run_bot():
    # Get token from credentials.json file
    discord_token = credentials.load_from_file('credentials.json')

    # If the token is None, exit.
    if discord_token == None:
        exit(1)

    # Create a discord client
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    
    # Add event handlers
    @client.event
    async def on_ready():
        print(client.user.name + ' is running.')

    @client.event
    async def on_message(msg):
        if msg.author == client.user:
            return
        
        await message.process_message(msg)

    # Try to run the bot
    try:
        client.run(discord_token)
    except Exception as e:
        print(format.error(str(e)))
        exit(1)