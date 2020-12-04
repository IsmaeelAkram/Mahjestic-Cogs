from redbot.core import commands, checks
from redbot.core.bot import Config, Red
import discord
import logging
import asyncio

class PersonalVoice(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2480938239048209)
        self.logger = logging.getLogger('red.mahjesticcogs.personalvoice')

    @commands.group(autohelp=True)
    async def personalvoice(self, ctx):
        """Personal Voice commands"""
        pass

    @personalvoice.group(name="category", autohelp=True)
    async def voice_category(self, ctx):
        """Category where new channels will be created."""
        pass
    @voice_category.command(name="set")
    @checks.admin_or_permissions(manage_channels=True)
    async def set_category(self, ctx: commands.Context, id: int):
        await self.config.guild(ctx.guild).voice_category.set(id)
        await ctx.channel.send(f"Voice category has been set to: **{discord.utils.get(ctx.guild.categories, id=id).name}** ({id})")
    @voice_category.command(name="get")
    @checks.admin_or_permissions(manage_channels=True)
    async def get_category(self, ctx: commands.Context):
        category_id = await self.config.guild(ctx.guild).voice_category()
        await ctx.channel.send(f"Voice category is set to: **{discord.utils.get(ctx.guild.categories, id=category_id).name}** ({category_id})")
    
    @personalvoice.group(name="channel", autohelp=True)
    async def voice_channel(self, ctx):
        """Voice channel to join and activate new channel."""
        pass
    @voice_channel.command(name="set")
    @checks.admin_or_permissions(manage_channels=True)
    async def set_channel(self, ctx: commands.Context, id: int):
        channel = await self.bot.fetch_channel(id)
        await self.config.guild(ctx.guild).voice_channel.set(id)
        await ctx.channel.send(f"Voice category has been set to: **{channel.name}** ({id})")
    @voice_channel.command(name="get")
    @checks.admin_or_permissions(manage_channels=True)
    async def get_channel(self, ctx: commands.Context):
        channel_id = await self.config.guild(ctx.guild).voice_channel()
        channel = await self.bot.fetch_channel(channel_id)
        await ctx.channel.send(f"Voice category is set to: **{channel.name}** ({channel.id})")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        category = await self.config.guild(member.guild).voice_category()
        channel = await self.config.guild(member.guild).voice_channel()
        
        if not after.channel:
            if before.channel != None:
                if before.channel.name == f"{member.name}'s Channel":
                    await before.channel.delete()
        else:
            if after.channel.id == channel:
                category = discord.utils.get(member.guild.categories, id=category)
                new_vc = await member.guild.create_voice_channel(f"{member.name}'s Channel", category=category)
                await member.move_to(new_vc)
            
