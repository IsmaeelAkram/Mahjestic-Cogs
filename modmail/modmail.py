from redbot.core import Config, commands
import discord
from discord.ext import commands as Commands

class Modmail(commands.Cog):
    """Simple modmail cog for Mahjestic Manor"""

    @commands.Cog.listener()
    async def on_message(self, ctx: Commands.Context):
        if(isinstance(ctx.channel, discord.channel.DMChannel)):
            await ctx.send("ModMail is coming soon to this bot")