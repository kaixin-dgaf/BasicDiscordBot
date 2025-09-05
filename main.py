import discord
from discord.ext import commands, tasks
import asyncio
import os
import sys
import traceback
from config import BOT_TOKEN, OWNER_IDS, DEV_IDS, ADMIN_IDS, emoji, DEFAULT_PREFIX
from utils.database import Database
from utils.helpers import get_prefix, is_authorized_user
from utils.logging import BotLogger

# Bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

class MentionResponseView(discord.ui.View):
    """View for bot mention response"""
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
    
    @discord.ui.button(label="Bot Stats", emoji=f"{emoji.server}", style=discord.ButtonStyle.primary)
    async def bot_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show bot statistics"""
        total_guilds = len(self.bot.guilds)
        total_users = sum(guild.member_count for guild in self.bot.guilds)
        total_channels = sum(len(guild.channels) for guild in self.bot.guilds)
        
        embed = discord.Embed(
            title=f"{self.bot.user.name} Statistics",
            color=0x2f3136
        )
        
        embed.add_field(name="Servers", value=f"{total_guilds:,}", inline=True)
        embed.add_field(name="Users", value=f"{total_users:,}", inline=True)
        embed.add_field(name="Channels", value=f"{total_channels:,}", inline=True)
        
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Python Version", value="3.11", inline=True)
        embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
        
        embed.set_footer(text=f"Bot ID: {self.bot.user.id}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="About Team", emoji=f"{emoji.user}", style=discord.ButtonStyle.secondary)
    async def about_team(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show information about the development team"""
        embed = discord.Embed(
            title="About the Development Team",
            color=0x2f3136
        )
        
        # Get owner information from config
        owner_user = self.bot.get_user(OWNER_IDS[0]) if OWNER_IDS else None
        owner_name = owner_user.name if owner_user else "Unknown"
        
        embed.add_field(
            name="Lead Developer",
            value=f"<@{OWNER_IDS[0]}> ({owner_name})",
            inline=False
        )
        
        embed.add_field(
            name="Bot Features",
            value="• Moderation & Administration\n• Welcome & Activity Systems\n• Voice Channel Management\n• Custom Embeds & Autoresponders\n• And much more!",
            inline=False
        )
        
        embed.add_field(
            name="Support",
            value="If you need help or have suggestions, feel free to contact the development team!",
            inline=False
        )
        
        embed.set_footer(text="Thank you for using our bot!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self.get_bot_prefix,
            intents=intents,
            help_command=None,
            case_insensitive=True
        )
        self.db = Database()
        self.owner_ids = OWNER_IDS
        self.logger = BotLogger(self)
        
    async def setup_hook(self):
        """Called when the bot is starting up"""
        # Initialize database
        await self.db.init_db()
        
        # Load all cogs
        cog_files = [
            'cogs.embed_builder.embed_builder',
            'cogs.welcomer.welcomer',
            'cogs.utility.utility',
            'cogs.owner.owner',
            'cogs.moderation.moderation',
            'cogs.vanityrole.vanityrole',
            'cogs.activityroles.activityroles',
            'cogs.customrole.customrole',
            'cogs.autorole.autorole',
            'cogs.voicemaster.voice',
            'cogs.media.media',
            'cogs.autoresponder.autoresponder',
            'cogs.help.help',
            'cogs.ignore.ignore',
            'cogs.antinuke.antinuke',
            'cogs.antinuke.monitoring',
            'cogs.automod.automod'
        ]
        
        for cog in cog_files:
            try:
                await self.load_extension(cog)
                print(f"✅ Loaded {cog}")
            except Exception as e:
                print(f"❌ Failed to load {cog}: {e}")
                traceback.print_exc()
        
        # Initialize logging webhooks
        await self.logger.initialize_webhooks()
        
        # Start background tasks
        self.vanity_checker.start()
        self.activity_checker.start()
        self.antinuke_cleanup.start()
    
    async def on_ready(self):
        """Called when the bot is ready"""
        print(f"🤖 {self.user} is now online!")
        print(f"📊 Connected to {len(self.guilds)} servers")
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} Guilds"
            )
        )
    
    async def on_guild_join(self, guild):
        """Called when bot joins a guild"""
        await self.logger.log_server_join(guild)
    
    async def on_guild_remove(self, guild):
        """Called when bot leaves a guild"""
        await self.logger.log_server_leave(guild)
    
    async def on_message(self, message):
        """Handle incoming messages"""
        # Ignore bot messages
        if message.author.bot:
            return
        
        # Check if message is in media channel
        if message.guild and hasattr(message, 'attachments'):
            is_media_channel = await self.db.is_media_channel(message.guild.id, message.channel.id)
            if is_media_channel:
                # Check if user has bypass
                has_bypass = await self.db.has_media_bypass(message.guild.id, message.author.id, message.author.roles)
                
                # If no attachment and no bypass, delete the message
                if not message.attachments and not has_bypass and not message.author.guild_permissions.manage_messages:
                    try:
                        await message.delete()
                        embed = discord.Embed(
                            title=f"{emoji.error} Media Only",
                            description="This channel only allows messages with attachments (images, videos, files).",
                            color=0xFF0000
                        )
                        warning_msg = await message.channel.send(embed=embed)
                        await asyncio.sleep(5)
                        await warning_msg.delete()
                        return
                    except discord.Forbidden:
                        pass
        
        # Check for bot mentions
        if self.user and self.user.mentioned_in(message) and not message.mention_everyone:
            # Only respond to direct mentions, not replies
            if f'<@{self.user.id}>' in message.content or f'<@!{self.user.id}>' in message.content:
                # Get server prefix (clean, not the command callable)
                prefix = await self.db.get_guild_prefix(message.guild.id) if message.guild else DEFAULT_PREFIX
                
                # Count total commands (excluding hidden ones)
                total_commands = 0
                for cog_name, cog in self.cogs.items():
                    if hasattr(cog, 'hidden') and getattr(cog, 'hidden', False):
                        continue
                    total_commands += len([cmd for cmd in cog.get_commands() if not cmd.hidden])
                
                bot_name = self.user.name if self.user else "Bot"
                bot_mention = self.user.mention if self.user else "@Bot"
                avatar_url = self.user.display_avatar.url if self.user else None
                
                embed = discord.Embed(
                    title=f"Hey! I'm {bot_name}",
                    description=f"**Current Prefix:** `{prefix}`\n**Total Commands:** {total_commands}\n\nType `{prefix}help` for command list!",
                    color=0x2f3136
                )
                
                if avatar_url:
                    embed.set_thumbnail(url=avatar_url)
                embed.set_footer(text="Use the buttons below for more information!")
                
                view = MentionResponseView(self)
                await message.reply(embed=embed, view=view, mention_author=False)
                return
        
        # Process commands normally
        await self.process_commands(message)
    
    async def get_bot_prefix(self, bot, message):
        """Get bot prefix - supports mentions and custom prefixes"""
        if self.user:
            prefixes = [f'<@{self.user.id}> ', f'<@!{self.user.id}> ']
        else:
            prefixes = []
        guild_prefix = await get_prefix(bot, message)
        if isinstance(guild_prefix, list):
            prefixes.extend(guild_prefix)
        else:
            prefixes.append(guild_prefix)
        return prefixes
    
    async def on_command_error(self, ctx, error):
        """Global error handler"""
        if isinstance(error, commands.CommandNotFound):
            # Show invalid command message
            prefix = await get_prefix(self, ctx.message)
            if isinstance(prefix, list):
                prefix = prefix[0]
            
            command_name = ctx.invoked_with
            embed = discord.Embed(
                title=f"{emoji.cross} Command Not Found",
                description=f"There is no command named `{command_name}`.",
                color=0x2f3136
            )
            await ctx.send(embed=embed, delete_after=5)
            return
        
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Missing Permissions",
                description=f"You don't have permission to use this command.\nRequired: {', '.join(error.missing_permissions)}",
                color=0x2f3136
            )
            await ctx.send(embed=embed, ephemeral=True)
            return
        
        if isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="❌ Bot Missing Permissions",
                description=f"I don't have permission to perform this action.\nRequired: {', '.join(error.missing_permissions)}",
                color=0x2f3136
            )
            await ctx.send(embed=embed, ephemeral=True)
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="❌ Missing Argument",
                description=f"Missing required argument: `{error.param.name}`",
                color=0x2f3136
            )
            await ctx.send(embed=embed, ephemeral=True)
            return
        
        # Log unexpected errors
        print(f"Unexpected error in {ctx.command}: {error}")
        traceback.print_exc()
        
        # Log to webhook
        error_context = f"Command: {ctx.command}\nGuild: {ctx.guild.name if ctx.guild else 'DM'}\nUser: {ctx.author}"
        await self.logger.log_error("Command Error", str(error), error_context)
        
        embed = discord.Embed(
            title="❌ Unexpected Error",
            description="An unexpected error occurred. Please try again later.",
            color=0x2f3136
        )
        await ctx.send(embed=embed, ephemeral=True)
    
    async def process_commands(self, message):
        """Custom command processing for no-prefix users"""
        if message.author.bot:
            return
        
        # Check if user is blacklisted
        blacklist_reason = await self.db.is_blacklisted_user(message.author.id)
        if blacklist_reason:
            return  # Silently ignore blacklisted users
        
        ctx = await self.get_context(message)
        
        # Check for no-prefix users
        if not ctx.valid and await is_authorized_user(self.db, message.author.id):
            # Try processing as a no-prefix command
            content = message.content.strip()
            if content and not content.startswith(('http', 'www', 'discord.gg')):
                # Create a fake prefix context
                message.content = f"?{content}"
                ctx = await self.get_context(message)
        
        # Check ignore settings before invoking command
        if ctx.valid and ctx.command:
            # Check if command should be ignored
            if await self._should_ignore_command(ctx):
                embed = discord.Embed(
                    title=f"{emoji.cross} Command Ignored",
                    description=f"The command `{ctx.command.name}` is ignored in this channel.",
                    color=0x2f3136
                )
                await ctx.send(embed=embed, delete_after=5)
                return
            
            # Log command execution
            await self.logger.log_command_executed(ctx)
        
        await self.invoke(ctx)
    
    async def _should_ignore_command(self, ctx):
        """Check if a command should be ignored"""
        if not ctx.guild:
            return False
        
        # Check if user has bypass permission
        user_role_ids = [role.id for role in ctx.author.roles] if hasattr(ctx.author, 'roles') else []
        if await self.db.is_ignore_bypassed(ctx.guild.id, ctx.channel.id, ctx.author.id, user_role_ids):
            return False
        
        # Get ignore settings for this channel
        ignore_settings = await self.db.get_ignore_setting(ctx.guild.id, ctx.channel.id)
        if not ignore_settings:
            return False
        
        # Check if all commands are ignored
        if ignore_settings.get('ignore_all'):
            return True
        
        # Check if specific command is ignored
        ignored_commands = ignore_settings.get('ignored_commands', '').split(',')
        ignored_commands = [cmd.strip().lower() for cmd in ignored_commands if cmd.strip()]
        if ctx.command.name.lower() in ignored_commands:
            return True
        
        # Check if command category is ignored
        ignored_categories = ignore_settings.get('ignored_categories', '').split(',')
        ignored_categories = [cat.strip().lower() for cat in ignored_categories if cat.strip()]
        if ctx.cog and ctx.cog.qualified_name.lower() in ignored_categories:
            return True
        
        return False
    
    @tasks.loop(seconds=30)
    async def vanity_checker(self):
        """Check for vanity URL changes in user activities"""
        try:
            vanity_configs = await self.db.get_all_vanity_configs()
            
            for config in vanity_configs:
                guild = self.get_guild(config['guild_id'])
                if not guild:
                    continue
                
                vanity_url = config['vanity_url']
                role_id = config['role_id']
                role = guild.get_role(role_id)
                
                if not role:
                    continue
                
                for member in guild.members:
                    if member.bot:
                        continue
                    
                    has_vanity = await self._check_user_has_vanity(member, vanity_url)
                    has_role = role in member.roles
                    
                    if has_vanity and not has_role:
                        # Add role
                        try:
                            await member.add_roles(role, reason="Vanity URL detected")
                            await self._log_vanity_action(guild, member, config, "added")
                        except discord.Forbidden:
                            pass
                    elif not has_vanity and has_role:
                        # Remove role
                        try:
                            await member.remove_roles(role, reason="Vanity URL removed")
                            await self._log_vanity_action(guild, member, config, "removed")
                        except discord.Forbidden:
                            pass
        except Exception as e:
            print(f"Error in vanity checker: {e}")
    
    @tasks.loop(seconds=60)
    async def activity_checker(self):
        """Check for activity changes"""
        try:
            activity_configs = await self.db.get_all_activity_configs()
            
            for config in activity_configs:
                guild = self.get_guild(config['guild_id'])
                if not guild:
                    continue
                
                activity_type = config['activity_type']
                role_id = config['role_id']
                role = guild.get_role(role_id)
                
                if not role:
                    continue
                
                for member in guild.members:
                    if member.bot:
                        continue
                    
                    has_activity = await self._check_user_has_activity(member, activity_type)
                    has_role = role in member.roles
                    
                    if has_activity and not has_role:
                        # Add role
                        try:
                            await member.add_roles(role, reason=f"{activity_type} activity detected")
                        except discord.Forbidden:
                            pass
                    elif not has_activity and has_role:
                        # Remove role
                        try:
                            await member.remove_roles(role, reason=f"{activity_type} activity removed")
                        except discord.Forbidden:
                            pass
        except Exception as e:
            print(f"Error in activity checker: {e}")

    @tasks.loop(hours=24)
    async def antinuke_cleanup(self):
        """Cleanup disabled antinuke configurations after 7 days"""
        try:
            cleaned_count = await self.db.cleanup_disabled_antinuke()
            if cleaned_count > 0:
                print(f"Cleaned up antinuke data for {cleaned_count} guilds")
        except Exception as e:
            print(f"Error in antinuke cleanup: {e}")
    
    async def _check_user_has_vanity(self, member, vanity_url):
        """Check if user has vanity URL in bio or activities"""
        import re
        
        # Extract the vanity code from the full URL
        vanity_patterns = [
            rf"discord\.gg/{re.escape(vanity_url)}",
            rf"\.gg/{re.escape(vanity_url)}",
            rf"https://discord\.gg/{re.escape(vanity_url)}"
        ]
        
        # Check activities/custom status
        for activity in member.activities:
            if hasattr(activity, 'state') and activity.state:
                for pattern in vanity_patterns:
                    if re.search(pattern, activity.state, re.IGNORECASE):
                        return True
            if hasattr(activity, 'name') and activity.name:
                for pattern in vanity_patterns:
                    if re.search(pattern, activity.name, re.IGNORECASE):
                        return True
        
        return False
    
    async def _check_user_has_activity(self, member, activity_type):
        """Check if user has specific activity type"""
        activity_map = {
            'playing': discord.ActivityType.playing,
            'listening': discord.ActivityType.listening,
            'streaming': discord.ActivityType.streaming,
            'competing': discord.ActivityType.competing
        }
        
        target_type = activity_map.get(activity_type.lower())
        if not target_type:
            return False
        
        for activity in member.activities:
            if activity.type == target_type:
                return True
        
        return False
    
    async def _log_vanity_action(self, guild, member, config, action):
        """Log vanity role actions"""
        log_channel_id = config.get('log_channel_id')
        if not log_channel_id:
            return
        
        log_channel = guild.get_channel(log_channel_id)
        if not log_channel:
            return
        
        if action == "added":
            message = f"Thank you {member.display_name} for proudly promoting our server vanity! You've been rewarded with a role."
        else:
            message = f"Since you are no longer promoting our vanity, your reward role has been removed."
        
        # Check if there's a custom embed
        custom_embed_name = config.get('custom_embed')
        if custom_embed_name:
            embed_data = await self.db.get_embed(guild.id, custom_embed_name)
            if embed_data:
                from utils.variables import parse_variables
                parsed_data = await parse_variables(embed_data, member, guild, log_channel)
                
                embed = discord.Embed(color=0x2f3136)
                if parsed_data.get('title'):
                    embed.title = parsed_data['title']
                if parsed_data.get('description'):
                    embed.description = parsed_data['description']
                if parsed_data.get('footer'):
                    embed.set_footer(text=parsed_data['footer'])
                if parsed_data.get('thumbnail'):
                    embed.set_thumbnail(url=parsed_data['thumbnail'])
                if parsed_data.get('author'):
                    embed.set_author(name=parsed_data['author'])
                
                for field in parsed_data.get('fields', []):
                    embed.add_field(name=field['name'], value=field['value'], inline=field.get('inline', False))
                
                await log_channel.send(embed=embed)
                return
        
        # Default embed
        embed = discord.Embed(
            description=message,
            color=0x2f3136
        )
        await log_channel.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    bot = DiscordBot()
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid bot token!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        sys.exit(1)
