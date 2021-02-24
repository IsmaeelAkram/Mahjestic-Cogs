from redbot.core import commands, checks
from redbot.core.bot import Config, Red
import discord
import logging
import re
import random
import string

class StealEmoji(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2430948239048209)
        self.logger = logging.getLogger('red.mahjesticcogs.stealemoji')

    async def steal_emoji(self, emoji_name: str, emoji_id: int, msg: discord.Message, guild: discord.Guild):
        emoji_url = "https://cdn.discordapp.com/emojis/<emoji_id>.png".replace("<emoji_id>", emoji_id)
        await msg.channel.send(embed=discord.Embed(title="Emoji stolen!", description="I just stole this emoji!").set_thumbnail(url=emoji_url))

        new_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        await guild.create_custom_emoji(name=(new_name), image=emoji_url)
        

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return

        emojis_text = re.findall(r'<:\w*:\d*>', msg.content)
        emojis = []
        for e in emojis_text:
            id = e.split(':')[2].replace('>', '')
            name = None
            emoji = self.bot.get_emoji(int(id))
            emojis.append((name, id))

        for emoji in emojis:
            guild = self.bot.get_guild(msg.guild.id)
            if guild != msg.guild.id:
                await self.steal_emoji(emoji[0], emoji[1], msg, guild)
