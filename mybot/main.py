from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext.commands import CheckFailure, CommandNotFound, Bot, MissingRequiredArgument, BadArgument
from commands import setup_commands  # Import command setup function

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# Set up bot with prefix "!"
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = Bot(command_prefix="!", intents=intents)

# Load commands from commands.py
setup_commands(bot)

async def load_cogs():
    await bot.load_extension("moderations")  # Load moderation commands

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await load_cogs()

# Ignore unknown command errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure):
        return await ctx.reply("❌ **You do not have permission to use this command!**")

    if isinstance(error, CommandNotFound):
        return await ctx.reply("⚠️ **The command does not exist.**\nUse **!cmds** or **!commands** to view available commands.")

    if isinstance(error, BadArgument):
        return await ctx.reply("❌ **Invalid argument! Please provide a correct one.**")

    if isinstance(error, MissingRequiredArgument):
        return await ctx.reply(f"❌ **Missing required argument: `{error.param.name}`. Please mention a member!**")

    await ctx.reply(f"❌ **An error occurred:** `{error}`")
    raise error  # Logs other unexpected errors

if __name__ == "__main__":
    bot.run(TOKEN)
