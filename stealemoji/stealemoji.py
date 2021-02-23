from redbot.core import commands, checks
from redbot.core.bot import Config, Red
import discord
import logging
import re

class StealEmoji(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2430948239048209)
        self.logger = logging.getLogger('red.mahjesticcogs.stealemoji')

    async def steal_emoji(self, emoji: discord.Emoji, msg: discord.Message):
        await msg.channel.send(embed=discord.Embed(title="Emoji stolen!", description="I just stole this emoji!").set_thumbnail(url=emoji.url))

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return

        emojis_text = re.findall(r'<:\w*:\d*>', msg.content)
        emojis = []
        for e in emojis_text:
            id = e.split(':')[2].replace('>', '')
            emoji = self.bot.get_emoji(int(id))
            emojis.append(emoji)

            self.logger.info(emoji)
            self.logger.info(msg.guild)
            if emoji.guild.id != msg.guild.id:
                await self.steal_emoji(emoji, msg)

        
