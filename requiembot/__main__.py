# Main bot program to connect to Discord and handle commands.
# Copyright (C) 2022 Michael Munzer
# This file is part of RequiemBot.
#
# RequiemBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# RequiemBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from traceback import format_exception

from . import __version__, parser

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if not (TOKEN := os.getenv("TOKEN")):
    print("Error: Bot token not found in environment variables or .env")
    exit()

intents = discord.Intents.default()
bot = commands.Bot(commands.when_mentioned, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ID={bot.user.id}")
    print("--------")


@bot.tree.command()
async def help(interaction: discord.Interaction):
    """Display the help dialog."""
    embed = discord.Embed(title="Help & Info", description="This bot can roll dice in tabletop RPGs. " +
                          "Included here are some common rolls for popular systems.\n\n" +
                          "For detailed info and source code, see GitHub:\n" +
                          "https://github.com/michaelmunzer/RequiemBot\n")
    embed.add_field(name="Roll", value="`d20+3`", inline=True)
    embed.add_field(name="5e Stat", value="`4d6k3`", inline=True)
    embed.add_field(name="Fudge/FATE", value="`4df`", inline=True)
    embed.add_field(name="Advantage", value="`2d20k1 - 1`", inline=True)
    embed.add_field(name="Disadvantage", value="`2d20kl1 + 3`", inline=True)
    embed.add_field(name="Wild Die", value="`1d6!`", inline=True)
    if bot.user.avatar:
        embed.set_footer(text=f"RequiemBot v{__version__}",
                         icon_url=bot.user.avatar.url)
    else:
        embed.set_footer(text=f"RequiemBot v{__version__}")
    await interaction.response.send_message(embed=embed)


@bot.tree.command()
@app_commands.describe(
    roll="Expression containing dice and/or math.",
    secret="If set to True, the roll and its result will only be visible to you. Default is False.",
    repeat="Amount of times to repeat the roll. Default is 1."
)
async def roll(interaction: discord.Interaction, roll: str, secret: bool = False, repeat: int = 1):
    """Roll dice and do math."""
    response = f"Rolled `{roll}`:"

    if repeat < 1:
        repeat = 1
    elif repeat > 1:
        response += f" {repeat} times"

    try:
        roll_tree = parser.parse(roll)
        rolls = []
        for i in range(repeat):
            rolls.append(roll_tree.evaluate())
    except (parser.ParseError, ZeroDivisionError, ValueError) as e:
        response += "\n**Error:** " + str(e)
        secret = True
    except Exception as e:
        response += "\n**Uncaught Error:**"
        response += "\nThis isn't your fault. Please notify this bot's creator or open an issue on GitHub. "
        response += "Include what you rolled, and this info:\n```\n"
        for i in format_exception(e):
            response += i
        response += "```"
    else:
        for val, string in rolls:
            response += f"\n{string} = **{val}**"

    if len(response) > 2000:
        await interaction.response.send_message(f"Rolled `{roll}`\n**Error:** Output is too long to send on Discord", ephemeral=True)
    else:
        await interaction.response.send_message(response, ephemeral=secret)


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def testing(ctx: commands.Context, spec: Optional[Literal["stop", "start", "guild"]] = None):
    if spec == "start":
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Started testing {len(synced)} commands in the current guild.")
    elif spec == "stop":
        ctx.bot.tree.clear_commands(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Stopped testing {len(synced)} commands in the current guild.")
    elif spec == "guild":
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(synced)} commands in the current guild.")
    else:
        synced = await ctx.bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} commands globally.")

try:
    bot.run(TOKEN)
except KeyboardInterrupt:
    bot.close()
