import discord
from discord.ext import commands, tasks
import config
import os
import itertools

# Enable necessary intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.get_prefix, help_command=None, intents=intents)

async def load_extensions():
    """Dynamically loads all cogs from subdirectories and prints folder names only."""
    for folder in os.listdir("cogs"):
        folder_path = os.path.join("cogs", folder)
        if os.path.isdir(folder_path):
            print(f"✅ Loaded {folder}")  # Show only the folder name in console
            for file in os.listdir(folder_path):
                if file.endswith(".py") and file != "__init__.py":
                    try:
                        await bot.load_extension(f"cogs.{folder}.{file[:-3]}")
                    except Exception:
                        pass  # Suppress individual file loading output

@bot.event
async def setup_hook():
    """Executed before the bot starts running, used to load cogs and sync commands."""
    await load_extensions()
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

# Define bot status cycle with correct lambda execution
def get_status():
    return itertools.cycle([
        discord.Game(name=f"Moderating {len(bot.guilds)} servers"),
        discord.Activity(type=discord.ActivityType.listening, name=f"{sum(g.member_count for g in bot.guilds)} users"),
        discord.Streaming(name="Faster than Light", url="https://www.twitch.tv/discord")  # Dummy URL required
    ])

status_cycle = get_status()

@tasks.loop(seconds=30)
async def change_status():
    """Cycles through different bot statuses."""
    status = next(status_cycle)
    await bot.change_presence(
        activity=status,
        status=discord.Status.online if isinstance(status, discord.Game)
        else discord.Status.dnd if isinstance(status, discord.Activity)
        else discord.Status.idle
    )

@bot.event
async def on_ready():
    """Executed when the bot is fully ready."""
    print(f"✅ Logged in as {bot.user}")
    if not change_status.is_running():
        change_status.start()

bot.run(config.TOKEN)