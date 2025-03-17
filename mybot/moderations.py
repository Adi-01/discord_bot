import discord
from discord.ext import commands
import asyncio
import json_utils  # Import our JSON utility

intents = discord.Intents.default()
intents.members = True

def is_admin():
    async def predicate(ctx):
        if ctx.author == ctx.guild.owner:
            return True
        if ctx.author.guild_permissions.administrator:
            return True
        else:
            await ctx.reply("❌ You need **Admin Access** to use this command!")
            return False
    return commands.check(predicate)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mute_tasks = {}

    def check_permissions(self, ctx, member: discord.Member):
        """Check if the command issuer has permission to act on the target user."""
        if member == ctx.author:
            return "❌ You **cannot** take action against **yourself**!"
        if member == ctx.guild.owner:
            return "❌ You **cannot** take action against the **server owner**!"
        if any(role.permissions.administrator for role in member.roles) and ctx.author != ctx.guild.owner:
            return f"❌ Only the **server owner** can take action against {member.mention}!"
        return None

    @commands.command(name="warn")
    @is_admin()
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Warn a user and take action if warning threshold is met."""
        error = self.check_permissions(ctx, member)
        if error:
            return await ctx.reply(error)

        warn_count = json_utils.add_warning(member.id, reason)
        await ctx.reply(f"⚠️ {member.mention} has been warned. Reason: {reason} (Warnings: {warn_count})")

        # Mute if warnings reach 3
        if warn_count == 3:
            await self.mute(ctx, member, duration=60)  # Mute for 1 minute
        # Ban if warnings reach 5
        elif warn_count >= 5:
            await self.ban(ctx, member, reason="Reached warning limit.")

    @commands.command(name="warnings")
    @is_admin()
    async def warnings(self, ctx, member: discord.Member):
        """Show warnings for a user."""
        warnings = json_utils.get_warnings(member.id)
        if not warnings:
            await ctx.reply(f"ℹ️ {member.mention} has no warnings.")
        else:
            warning_list = "\n".join([f"{i+1}. {w}" for i, w in enumerate(warnings)])
            await ctx.reply(f"⚠️ Warnings for {member.mention}:\n{warning_list}")

    @commands.command(name="clearwarnings")
    @is_admin()
    async def clear_warnings(self, ctx, member: discord.Member):
        """Clear all warnings for a user."""
        json_utils.clear_warnings(member.id)
        await ctx.reply(f"✅ Cleared all warnings for {member.mention}.")

    @commands.command(name="ban")
    @is_admin()
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member and store in the ban list."""
        error = self.check_permissions(ctx, member)
        if error:
            return await ctx.reply(error)

        await member.ban(reason=reason)
        json_utils.add_ban(member.id, reason)
        await ctx.reply(f"✅ {member.mention} has been banned. Reason: {reason}")

    @commands.command(name="mute")
    @is_admin()
    async def mute(self, ctx, member: discord.Member, duration: int = 60):
        """Mute a user for a specified duration (in seconds)."""
        error = self.check_permissions(ctx, member)
        if error:
            return await ctx.reply(error)

        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted", reason="Mute role for moderation")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False, speak=False)

        # Store removed admin roles only for mute
        removed_roles = [role.id for role in member.roles if role.permissions.administrator]
        if removed_roles:
            await member.remove_roles(*[ctx.guild.get_role(role_id) for role_id in removed_roles])
            json_utils.store_removed_roles(member.id, removed_roles)  # Save to JSON

        await member.add_roles(mute_role)
        json_utils.add_mute(member.id, duration)
        await ctx.reply(f"🔇 {member.mention} has been muted for {duration} seconds.")

        # Prevent duplicate mute tasks
        if member.id in self.mute_tasks:
            self.mute_tasks[member.id].cancel()

        self.mute_tasks[member.id] = asyncio.create_task(self.scheduled_unmute(ctx, member, duration))

    async def scheduled_unmute(self, ctx, member, duration):
        """Handles scheduled unmute after duration"""
        await asyncio.sleep(duration)
        await self.unmute(ctx, member, scheduled=True)
        await ctx.reply(f"🔊 {member.mention} has been **unmuted**.")

    @commands.command(name="unmute")
    @is_admin()
    async def unmute(self, ctx, member: discord.Member, scheduled=False):
        """Unmute a user by removing the Muted role and restoring admin roles."""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            return await ctx.reply("⚠️ There is no 'Muted' role in this server.")

        if mute_role not in member.roles:
            return await ctx.reply(f"ℹ️ {member.mention} is not muted.")

        await member.remove_roles(mute_role)

        # Restore previous admin roles if they were removed
        removed_roles = json_utils.get_removed_roles(member.id)
        if removed_roles:
            await member.add_roles(*[ctx.guild.get_role(role_id) for role_id in removed_roles])
            json_utils.clear_removed_roles(member.id)  # Remove stored roles after restoring

        json_utils.remove_mute(member.id)  # Remove mute entry from storage

        # Prevent duplicate unmute messages
        if not scheduled:
            await ctx.reply(f"🔊 {member.mention} has been **unmuted**.")

        # Cleanup mute task
        if member.id in self.mute_tasks:
            self.mute_tasks[member.id].cancel()
            del self.mute_tasks[member.id]

    @commands.command(name="banlist")
    @is_admin()
    async def banlist(self, ctx):
        """Show all banned users and their reasons."""
        bans = json_utils.load_data().get("bans", {})
        if not bans:
            return await ctx.reply("ℹ️ No users are currently banned.")

        ban_info = "\n".join([f"🔴 **User ID:** `{uid}` | **Reason:** {reason}" for uid, reason in bans.items()])
        await ctx.reply(f"📜 **Ban List:**\n{ban_info}")

    @commands.command(name="mutedlist")
    @is_admin()
    async def mutedlist(self, ctx):
        """Show all muted users and their mute durations."""
        mutes = json_utils.load_data().get("mutes", {})
        if not mutes:
            return await ctx.reply("ℹ️ No users are currently muted.")

        mute_info = "\n".join([f"🔇 **User ID:** `{uid}` | **Duration:** {duration}s" for uid, duration in mutes.items()])
        await ctx.reply(f"📜 **Muted Users:**\n{mute_info}")
    
    @commands.command(name="id")
    @is_admin()
    async def get_id(self, ctx, member: discord.Member = None):
        """Get the user ID of a mentioned user or yourself."""
        member = member or ctx.author  # If no one is mentioned, use command sender
        await ctx.reply(f"🆔 {member.name}'s ID: `{member.id}`")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
