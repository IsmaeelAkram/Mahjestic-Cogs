from redbot.core import commands
from redbot.core.bot import Config, Red
import discord
from discord.ext import commands as Commands

class Modmail(commands.Cog):
    """Simple modmail cog"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2480948239048209)

   