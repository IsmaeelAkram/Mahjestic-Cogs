from redbot.core import commands, checks
from redbot.core.bot import Config, Red
import discord
import tweepy
from tweepy.error import TweepError
import logging
import asyncio

class Tweet(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2480948239048209)
        self.logger = logging.getLogger('red.mahjesticcogs.tweet')

    async def tweet(self, message: discord.Message):
        consumer_key, consumer_secret = await self.config.guild(message.guild).consumer_key(), await self.config.guild(message.guild).consumer_secret()
        access_token, access_secret = await self.config.guild(message.guild).access_token(), await self.config.guild(message.guild).access_secret()
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        api.update_status(message.content)
        await message.add_reaction('✅')

    @commands.command()
    @checks.admin_or_permissions(manage_channels=True)
    @commands.guild_only()
    async def tweet_guide(self, ctx):
        """Guide on how to setup cog"""
        guide = "**Step #1: Create a Twitter Developer App**\nThis is required to do by the user because an app is tied to a Twitter account. Whichever account the app is created on, is the account that tweets will be posted on. To make an app, [go to the dev portal](https://developer.twitter.com/en/portal/projects-and-apps), scroll down, and click **Create App**. Name it whatever you want, and go to the settings of the app.\n\n**#2: Change app permissions to read and write**\nIn the app settings, click on **Edit** near **App permissions**, change the permissions to **Read And Write**, and click **Save**.\n\n**Step #3: Get credentials!**\nOn the top of Settings, click **Keys and tokens**. Here, you can find your access token, access secret, consumer key, and consumer secret. You can set these using `[p]set_twitter_credentials <consumer_key> <consumer_secret> <access_token> <access_secret>`.\n\n**Step #4: Set the tweet channel**\nNow you just have to set the channel you want to listen for tweets in. You can do this using `[p]set_tweet_channel <channel>`. That's it! It's all set up. Now, every message sent in that channel will be tweeted."
        await ctx.channel.send(embed=discord.Embed(title="Tweet Guide", description=guide))
    
    @commands.command()
    @checks.admin_or_permissions(manage_channels=True)
    @commands.guild_only()
    async def set_twitter_credentials(self, ctx, consumer_key: str, consumer_secret: str, access_token: str, access_secret: str):
        """Set twitter auth credentials. You'll need to make a Twitter Developer app to get these."""
        await self.config.guild(ctx.guild).consumer_key.set(consumer_key)
        await self.config.guild(ctx.guild).consumer_secret.set(consumer_secret)
        await self.config.guild(ctx.guild).access_token.set(access_token)
        await self.config.guild(ctx.guild).access_secret.set(access_secret)
        await ctx.channel.send("Done!")

    @commands.command()
    @commands.guild_only()
    @checks.admin_or_permissions(manage_channels=True)
    async def set_tweet_channel(self, ctx, channel: discord.TextChannel):
        """Set channel to listen for messages"""
        await self.config.guild(ctx.guild).tweet_channel.set(channel.id)
        await ctx.channel.send(f"Tweet channel has been set to: <#{channel.id}>")

    @commands.command()
    @commands.guild_only()
    @checks.admin_or_permissions(manage_channels=True)
    async def get_tweet_channel(self, ctx):
        """Get channel being listened for messages"""
        tweet_channel = await self.config.guild(ctx.guild).tweet_channel()
        await ctx.channel.send(f"Tweet channel is set to: <#{tweet_channel}>")


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Stop if message is from bot
        if message.author.id == self.bot.user.id:
            return

        tweet_channel = await self.config.guild(message.guild).tweet_channel()
        if message.channel.id == tweet_channel:
            consumer_key, consumer_secret = await self.config.guild(message.guild).consumer_key(), await self.config.guild(message.guild).consumer_secret()
            access_token, access_secret = await self.config.guild(message.guild).access_token(), await self.config.guild(message.guild).access_secret()
            if not consumer_key or not consumer_secret or not access_token or not access_secret:
                await message.add_reaction("❌")
                await message.channel.send("You need to set your Twitter API Credentials with `[p]set_twitter_credentials`.")
                return
            self.logger.info(f'Tweeted "{message.content}"')
            try:
                await self.tweet(message)
            except TweepError as e:
                if e.api_code == 89:
                    await message.add_reaction("❌")
                    await message.channel.send("Your Twitter API credentials are invalid.")
                    return
                else:
                    await message.add_reaction("❌")
                    await message.channel.send("An error has occurred. Run traceback to find the error.")
                    return