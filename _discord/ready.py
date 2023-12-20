from discord import Client
from discord.ext.commands import Cog

class Ready(Cog):
    def __init__(self, bot: Client):
        self.bot = bot

    @Cog.listener('on_ready')
    async def ready(self):
        print(f'{self.bot.user} logado')

def setup(bot):
    bot.add_cog(Ready(bot))