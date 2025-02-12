import discord
from discord.ext import commands
import config

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_error_embed(self, ctx, title, description):
        """Sends an error embed."""
        embed = discord.Embed(title=title, description=description, color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="ban", description="Bans a member permanently or for a specific duration.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, duration: str = None, *, reason: str = "No reason provided"):
        """Bans a member permanently or for a specific duration."""
        if not member:
            return await self.send_error_embed(ctx, "Incorrect Usage ❌", "**Usage:** `/ban @user [duration] [reason]`\n**Example:** `/ban @User 7d Breaking rules`")

        # Prevent self-ban
        if member.id == ctx.author.id:
            return await self.send_error_embed(ctx, "Action Denied 🚫", "**You can't ban yourself!**")

        # Prevent banning the bot itself
        if member.id == ctx.bot.user.id:
            return await ctx.send("**You can't ban me, __Dumbo__!**")

        # Prevent banning the server owner
        if member == ctx.guild.owner:
            return await self.send_error_embed(ctx, "Action Denied 🚫", "**You can't ban the server owner!**")

        # Prevent banning someone with a higher or equal role
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await self.send_error_embed(ctx, "Action Denied 🚫", f"**You can't ban {member.mention} because they have a higher or equal role!**")

        # Attempt to ban
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Banned ⛔",
                description=f"**{member.mention} has been banned!**\n"
                            f"**Reason:** `{reason}`",
                color=config.DEFAULT_COLOR
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await self.send_error_embed(ctx, "Permission Error 🚫", "**I don't have permission to ban this user!**")

    @commands.hybrid_command(name="unban", description="Unbans a previously banned member.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int = None):
        """Unbans a user by ID"""
        if not user_id:
            return await self.send_error_embed(ctx, "Incorrect Usage ❌", "**Usage:** `/unban <user_id>`\n**Example:** `/unban 123456789012345678`")

        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            embed = discord.Embed(
                title="Unbanned ✅",
                description=f"**{user.mention} has been unbanned!**",
                color=config.DEFAULT_COLOR
            )
            await ctx.send(embed=embed)
        except discord.NotFound:
            await self.send_error_embed(ctx, "Error ⚠", "**User not found in the ban list!**")
        except discord.Forbidden:
            await self.send_error_embed(ctx, "Permission Error 🚫", "**I don't have permission to unban this user!**")

async def setup(bot):
    await bot.add_cog(Ban(bot))