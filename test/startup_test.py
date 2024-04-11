from discord.ext import commands
import os
import sys
import discord

import credentials

TOKEN = credentials.load_from_file('test-credentials.json')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
target_id = "ID of bot to be tested"
channel_id = "ID of channel of where it will be tested"

#@bot.command(name="help")
async def test_help(ctx):
    correct_response = 'Pong!'
    channel = await bot.fetch_channel(channel_id)
    await channel.send("help")

    def check(m):
        return m.content == correct_response and m.author.id == target_id

    response = await bot.wait_for('message', check=check)
    assert (response.content == correct_response)

bot.run(TOKEN)