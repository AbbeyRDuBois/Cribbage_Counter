###########################################################
# File: bot.py
#
# Authors: Andrew Rice, Bryce Schultz
# Date: 4/7/2024
#
# Description: This file contains the main bot loop.
###########################################################

#Foreign imports
import discord
import os

#Local imports
import message
import credentials
import format
import game

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
    tree = discord.app_commands.CommandTree(client)

    @tree.command(
        name="hand",
        description="Get your current hand",
        guild=discord.Object(id=1226726956301815848)
    )
    async def hand_command(interaction):
        try:
            hand_pic = await game.get_hand_pic(game.players.index(interaction.user))
            await interaction.response.send_message(content="Number in center of card is index.", file=discord.File(hand_pic), ephemeral=True)
            os.remove(hand_pic)
        except:
            await interaction.response.send_message("You need to !join and !start before you can get your hand.", ephemeral=True)

    @tree.command(
        name="calcs",
        description="Get the most recent hand calcs",
        guild=discord.Object(id=1226726956301815848)
    )
    async def calc_command(interaction):
        if game.calc_string == "":
            await interaction.response.send_message("You need to finish a round before you can see the hand values.", ephemeral=True)
        else:
            await interaction.response.send_message(game.calc_string, ephemeral=True)

    @client.event
    async def on_message(msg):
        if msg.author == client.user:
            return
        
        await message.process_message(msg)

    #On startup, sync command tree
    @client.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=1226726956301815848))
        print("Cribbage Bot is ready!")

    # Try to run the bot
    try:
        client.run(discord_token)
    except Exception as e:
        print(format.error(str(e)))
        exit(1)