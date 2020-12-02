from .tweet import Tweet

def setup(bot):
    bot.add_cog(Tweet(bot))