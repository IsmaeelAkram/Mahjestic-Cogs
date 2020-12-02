from redbot.core import commands, checks
from redbot.core.bot import Config, Red
import discord
from discord.ext import commands as Commands
import logging
import asyncio

class AmongUsLobby(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2480948239048209)
        self.logger = logging.getLogger('red.mahjesticcogs.amonguslobby')

    async def ask_for_code(self, member: discord.Member):
        await member.send(embed=discord.Embed(description="You joined the Among Us channel. Send your game code to start automated matchmaking. (Example: PQWOY)").set_footer(text="Write no to stop asking."))
        def check(message: discord.Message):
            return message.author.id == member.id
        try:
            code = await self.bot.wait_for('message', check=check, timeout=300)
            if(code.content == "no"):
                return
        except asyncio.TimeoutError:
            await member.send(embed=discord.Embed(description="You took more than 5 minutes to enter your Among Us code. Re-join the Among Us channel to start automated matchmaking."))
            return
        await member.send(embed=discord.Embed(description="Cool! I'm sending your Among Us code in chat as we speak."))
        return code

    async def send_code(self, code: discord.Message, after: discord.VoiceState, guild: discord.Guild):
        embed = discord.Embed(
            title=f"Code: {code.content}",
            description=f"{code.author.name} started an Among Us game!\n\nJoin **{after.channel.name}** to play!"
            ).set_thumbnail(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/4b1ceee5-9458-4434-80bc-fc5d83a2ea88/de5dkfo-361fa49d-4f48-432b-a55d-c9dad5fc5055.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvNGIxY2VlZTUtOTQ1OC00NDM0LTgwYmMtZmM1ZDgzYTJlYTg4XC9kZTVka2ZvLTM2MWZhNDlkLTRmNDgtNDMyYi1hNTVkLWM5ZGFkNWZjNTA1NS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.KPxCEBilI2yzC4kbrECS07aXWy4SGKXTrJ9DjMBgu8E")
        
        channel_id = await self.config.guild(guild).code_channel()
        channel = await self.bot.fetch_channel(channel_id)
        await channel.send(embed=embed)

    async def start_matchmaking(self, member: discord.Member, after: discord.VoiceState):
        code = await self.ask_for_code(member)
        await self.send_code(code, after, member.guild)

    @commands.group(autohelp=True)
    async def amongus(self, ctx):
        """Among us lobby commands"""
        pass

    @amongus.group(autohelp=True)
    async def voice_channel(self, ctx):
        """Among Us voice channel commands"""
        pass

    @amongus.group(autohelp=True)
    async def code_channel(self, ctx):
        """Code channel commands"""
        pass

    @voice_channel.command(name="set")
    @checks.admin_or_permissions(manage_channels=True)
    async def set_voice_channel(self, ctx: Commands.Context, voice_channel_id: int):
        """Get Among Us voice channel"""
        await self.config.guild(ctx.guild).voice_channel.set(voice_channel_id)
        await ctx.channel.send(embed=discord.Embed(description=f"Among Us voice channel has been set to: **{voice_channel_id}**"))

    @voice_channel.command(name="get")
    @checks.admin_or_permissions(manage_channels=True)
    async def get_voice_channel(self, ctx: Commands.Context):
        """Set Among Us voice channel"""
        voice_channel_id = await self.config.guild(ctx.guild).voice_channel()
        await ctx.channel.send(embed=discord.Embed(description=f"Among Us voice channel is set to: **{voice_channel_id}**"))

    @code_channel.command(name="set")
    @checks.admin_or_permissions(manage_channels=True)
    async def set_code_channel(self, ctx: Commands.Context, channel: discord.TextChannel):
        """Set code channel"""
        await self.config.guild(ctx.guild).code_channel.set(channel.id)
        await ctx.channel.send(embed=discord.Embed(description=f"Among Us code channel has been set to: **{channel.mention}**"))

    @code_channel.command(name="get")
    @checks.admin_or_permissions(manage_channels=True)
    async def get_code_channel(self, ctx: Commands.Context):
        """Get code channel"""
        channel_id = await self.config.guild(ctx.guild).code_channel()
        channel = await self.bot.fetch_channel(channel_id)
        await ctx.channel.send(embed=discord.Embed(description=f"Among Us code channel is set to: **{channel.mention}**"))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        voice_channel_id = await self.config.guild(member.guild).voice_channel()
        if after.channel is not None:
            if after.channel.id == voice_channel_id:
                self.logger.info(f"{member.name} joined the Among Us channel.")
                await self.start_matchmaking(member, after)
    