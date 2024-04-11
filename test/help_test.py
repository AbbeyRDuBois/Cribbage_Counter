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
import os
import sys
import discord

# Local imports
import credentials
import helper

token = credentials.load_from_file('test-credentials.json')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

async def test_help():
    correct_response = 'test'
    channel = await bot.fetch_channel(helper.test_channel_id)
    await channel.send("help")

    def check(m):
        return m.content == correct_response and m.author.id == helper.test_bot_id

    response = await bot.wait_for('message', check=check)
    assert (response.content == correct_response)

bot.run(token)