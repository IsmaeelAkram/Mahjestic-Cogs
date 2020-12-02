from redbot.core import commands
from redbot.core.bot import Config, Red
import discord
import logging
import datetime
from discord.ext import commands as Commands

from .thread import Thread

class Modmail(commands.Cog):
    """Simple modmail cog"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.guild_id = 525413739407867904
        self.config = Config.get_conf(self, identifier=2480948239048209)
        self.logger = logging.getLogger('red.mahjesticcogs.modmail')

    def get_thread_from_json(self, json: dict):
        return Thread(json['member_id'], json['messages'], json['created_at'])

    async def init_threads(self):
        await self.config.guild_from_id(self.guild_id).threads.set([])

    async def create_user_thread(self, member: discord.Member, initial_message: discord.Message, created_at: datetime.datetime):
        async with self.config.guild_from_id(self.guild_id).threads() as threads:
            threads.append(Thread(member.id, [initial_message.id], int(datetime.datetime.utcnow().timestamp())).json())

    async def get_user_thread(self, member: discord.Member):
        threads = await self.config.guild_from_id(self.guild_id).threads()
        for thread in threads:
            if thread['member_id'] == member.id:
                return thread
        return None

    @commands.command()
    async def threads(self, ctx: Commands.Context):
        threads = await self.config.guild_from_id(self.guild_id).threads()
        embed = discord.Embed(title="ModMail Threads")
        for thread_json in threads:
            thread = self.get_thread_from_json(thread_json)
            # embed.add_field(name=f"{member.name} ({member_id})", value="Thread")
        await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is not None:
            return
        if message.author.bot:
            return

        threads = await self.config.guild_from_id(self.guild_id).threads()
        if not threads:
            await self.init_threads()
        
        user_thread = await self.get_user_thread(message.author)
        if not user_thread:
            await self.create_user_thread(message.author, message, datetime.datetime.now())
            await message.add_reaction("✅")
            await message.channel.send(embed=discord.Embed(title="Thread Created", description="A staff member will be with you shortly."))
        else:
            await message.add_reaction("✅")