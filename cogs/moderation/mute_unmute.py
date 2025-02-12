from discord.ext import commands
import config

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_error_embed(self, ctx, title, description):
        """Sends an error embed."""
        embed = discord.Embed(title=title, description=description, color=discord.Color.red())
        await ctx.send(embed=embed)

    # Mute Command (Prefix & Slash)
    @commands.hybrid_command(name="mute", aliases=["shut", "timeout"], description="Mutes a member for a specific duration (default: 10 minutes).")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member = None, duration: str = "10m", *, reason: str = "No reason provided"):
        """Mutes a member for a specified duration (default: 10 minutes)."""
        if not member:
            return await self.send_error_embed(ctx, "Incorrect Usage ❌", "**Usage:** `/mute @user [duration] [reason]`\n**Example:** `/mute @User 30m Spamming`")

        # Prevent self-mute
        if member.id == ctx.author.id:
            return await self.send_error_embed(ctx, "Action Denied 🚫", "**You can't mute yourself!**")

        # Prevent muting the bot itself
        if member.id == ctx.bot.user.id:
            return await ctx.send("**You can't mute me, __Dumbo__!**")

        # Prevent muting the server owner
        if member == ctx.guild.owner:
            return await self.send_error_embed(ctx, "Action Denied 🚫", "**You can't mute the server owner!**")

        # Prevent muting someone with a higher or equal role
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await self.send_error_embed(ctx, "Action Denied 🚫", f"**You can't mute {member.mention} because they have a higher or equal role!**")

        # Convert duration to minutes
        time_units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        try:
            time_value = int(duration[:-1])
            time_unit = duration[-1].lower()
            if time_unit not in time_units:
                raise ValueError
            mute_duration = discord.utils.utcnow() + discord.utils.timedelta(seconds=time_value * time_units[time_unit])
        except ValueError:
            return await self.send_error_embed(ctx, "Invalid Duration ⚠", "**Use format:** `10m`, `2h`, `1d`")

        # Attempt to mute
        try:
            await member.timeout(mute_duration, reason=reason)
            embed = discord.Embed(
                title="Muted 🔇",
                description=f"**{member.mention} has been muted!**\n"
                            f"**Duration:** `{duration}`\n"
                            f"**Reason:** `{reason}`",
                color=config.DEFAULT_COLOR
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await self.send_error_embed(ctx, "Permission Error 🚫", "**I don't have permission to mute this user!**")

    # Unmute Command (Prefix & Slash)
    @commands.hybrid_command(name="unmute", description="Unmutes a muted member.")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member = None):
        """Unmutes a member"""
        if not member:
            return await self.send_error_embed(ctx, "Incorrect Usage ❌", "**Usage:** `/unmute @user`")

        try:
            await member.timeout(None)
            embed = discord.Embed(
                title="Unmuted 🔊",
                description=f"**{member.mention} has been unmuted!**",
                color=config.DEFAULT_COLOR
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await self.send_error_embed(ctx, "Permission Error 🚫", "**I don't have permission to unmute this user!**")

async def setup(bot):
    await bot.add_cog(Mute(bot))