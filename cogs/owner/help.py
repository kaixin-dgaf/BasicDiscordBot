import discord
from discord.ext import commands
from discord import app_commands
import config

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_help_embed(self, interaction_or_ctx, command_name=None):
        """Sends the help embed for both prefix and slash commands"""
        prefix = await config.get_prefix(self.bot, interaction_or_ctx) if isinstance(interaction_or_ctx, commands.Context) else "/"
        
        # Get the user's avatar (handling None cases properly)
        author = interaction_or_ctx.author if isinstance(interaction_or_ctx, commands.Context) else interaction_or_ctx.user
        avatar_url = (author.avatar or author.default_avatar).replace(static_format="png").url
        bot_avatar_url = (self.bot.user.avatar or self.bot.user.default_avatar).replace(static_format="png").url

        if command_name is None:
            embed = discord.Embed(
                title="Help Menu",
                description=f"Use `{prefix}help <command>` for more info on a command.\nExample: `{prefix}help mute`",
                color=config.DEFAULT_COLOR
            )
            embed.add_field(
                name="📌 Categories", 
                value="🔹 Antinuke\n🔹 AutoResponder\n🔹 Fun\n🔹 Information\n🔹 Moderation\n🔹 Utility\n🔹 Voice\n🔹 Welcome",
                inline=False
            )
            embed.set_thumbnail(url=bot_avatar_url)  # Bot's avatar as thumbnail
            embed.set_footer(text=f"Requested by {author}", icon_url=avatar_url)

            if isinstance(interaction_or_ctx, commands.Context):
                await interaction_or_ctx.send(embed=embed)
            else:
                await interaction_or_ctx.response.send_message(embed=embed)
            return

        command = self.bot.get_command(command_name)

        # Prevent showing help for the help command itself
        if command and command.name != "help":
            embed = discord.Embed(
                title=f"Command: `{prefix}{command.name}`",
                description=command.help or "No description available.",
                color=config.DEFAULT_COLOR
            )
            embed.add_field(
                name="Aliases",
                value=", ".join(command.aliases) if command.aliases else "None",
                inline=False
            )
            embed.set_thumbnail(url=bot_avatar_url)  # Bot's avatar as thumbnail
            embed.set_footer(text=f"Requested by {author}", icon_url=avatar_url)

            if isinstance(interaction_or_ctx, commands.Context):
                await interaction_or_ctx.send(embed=embed)
            else:
                await interaction_or_ctx.response.send_message(embed=embed)
        else:
            if isinstance(interaction_or_ctx, commands.Context):
                await interaction_or_ctx.send(f"❌ Command `{command_name}` not found.")
            else:
                await interaction_or_ctx.response.send_message(f"❌ Command `{command_name}` not found.", ephemeral=True)

    @commands.command()
    async def help(self, ctx, command_name=None):
        """Custom Help Command (Prefix)"""
        await self.send_help_embed(ctx, command_name)

    @app_commands.command(name="help", description="Get a list of available commands or details about a specific command.")
    async def slash_help(self, interaction: discord.Interaction, command_name: str = None):
        """Custom Help Command (Slash)"""
        await self.send_help_embed(interaction, command_name)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))