import discord
from discord.ext import commands
from random import randint

def setup_commands(bot: commands.Bot):
    """Registers all bot commands."""

    @bot.command(name="cmds",aliases=["commands"])
    async def cmds(ctx):
        """Shows a list of available commands and their descriptions."""
        embed = discord.Embed(
            title="📜 Bot Commands",
            description="Here are the available commands:",
            color=discord.Color.blue()
        )

        embed.add_field(name="🎲 `!roll`", value="Rolls a dice (1-6).", inline=False)
        embed.add_field(name="👋 `!hello`", value="Sends a greeting message.", inline=False)
        embed.add_field(name="📸 `!av @User`", value="Displays a user's profile picture.", inline=False)
        embed.add_field(name="🔇 `!mute @User [seconds]`", value="Mutes the user for the given time.", inline=False)
        embed.add_field(name="🔊 `!unmute @User`", value="Unmutes the user manually.", inline=False)
        embed.add_field(name="🚪 `!kick @User [reason]`", value="Kicks a user from the server.", inline=False)
        embed.add_field(name="🔨 `!ban @User [reason]`", value="Bans a user from the server.", inline=False)
        embed.add_field(name="⚠ `!warn @User [reason]`", value="Warns a user with punishment based on warn counts.", inline=False)
        embed.add_field(name="📜 `!cmds or !commands`", value="Displays this help message.", inline=False)

        embed.set_footer(text="Use these commands wisely! 😉")
        await ctx.reply(embed=embed)

    @bot.command(name="roll")
    async def roll_dice(ctx):
        """Rolls a dice and returns a number between 1 and 6."""
        await ctx.reply(f'🎲 You rolled: {randint(1, 6)}')

    @bot.command(name="hello")
    async def say_hello(ctx):
        """Sends a greeting message."""
        await ctx.reply("👋 Hello there!")
        
    @bot.command(name="av")
    async def profile(ctx, member: discord.Member = None):
        """Displays a user's profile picture."""
        member = member or ctx.author  # If no member is mentioned, use the command sender

        embed = discord.Embed(title=f"{member.name}'s Profile Picture", color=discord.Color.blue())
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)

        await ctx.reply(embed=embed)
