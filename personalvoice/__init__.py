from .personalvoice import PersonalVoice

def setup(bot):
    bot.add_cog(PersonalVoice(bot))