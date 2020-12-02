from redbot.core import Config, commands
import discord
from discord.ext import commands as Commands

class Modmail(commands.Cog):
    """Simple modmail cog"""

    @commands.Cog.listener()
    async def on_message(self, ctx: Commands.Context):
        if not ctx.message.guild:
            await ctx.channel.send("ModMail is coming soon to this bot.")