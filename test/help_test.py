###########################################################
# File: help_test.py
#
# Authors: Bryce Schultz
# Date: 4/10/2024
#
# Description: This file tests the help command.
###########################################################

# Foreign imports
from discord.ext import commands
import discord

# Local imports
import credentials
import helper

token = credentials.load_from_file('test-credentials.json')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
bot.remove_command('help')

__test__ = False
@bot.command(name='test-help')
async def test_ping(ctx):
    correct_response = 'Pong!'
    channel = await bot.fetch_channel(helper.test_channel_id)
    await channel.send('!help')

    def check(m):
        return m.content == correct_response and m.author.id == helper.bot_to_test_id

    response = await bot.wait_for('message', check=check)
    assert (response.content == correct_response)

bot.run(token)