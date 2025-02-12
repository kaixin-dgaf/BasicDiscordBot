import discord
from discord.ext import commands
import os
import datetime
import json
import sys
from typing import Set

print("Python version:", sys.version)


def load_data():
    try:
        with open("data.json", "r") as f:
            data = f.read()
            return json.loads(data) if data.strip() else {
                "prefixes": {},
                "no_prefix_users": []
            }
    except (FileNotFoundError, json.JSONDecodeError):
        return {"prefixes": {}, "no_prefix_users": []}


def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


def get_prefix(bot, message):
    data = load_data()
    return data["prefixes"].get(str(message.guild.id), "?")


class Bot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=self.dynamic_prefix, intents=intents)
        self.no_prefix_users = set(load_data().get("no_prefix_users", []))
        self.launch_time = datetime.datetime.utcnow()
        self.owner_ids = {1326586828739838003, 883997337863749652}

    async def dynamic_prefix(self, bot, message):
        if message.author.id in self.no_prefix_users:
            return ""
        return get_prefix(bot, message)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self):

        try:
            await self.load_extension("jishaku")
            print("Jishaku Loaded")
        except Exception as e:
            print(f"Failed to load Jishaku: {e}")

        for filename in os.listdir("./cogs/commands"):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.commands.{filename[:-3]}')
                    print(f'Loaded Cog: `{filename[:-3]}`')
                except Exception as e:
                    print(f"Failed to load Cog {filename}: {e}")


bot = Bot()
bot.run(os.environ['TOKEN'])
