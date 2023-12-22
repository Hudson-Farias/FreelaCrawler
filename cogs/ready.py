from discord import Client
from discord.ext.commands import Cog

from utils.dashboard import dashboard

class Ready(Cog):
    def __init__(self, bot: Client):
        self.bot = bot

    @Cog.listener('on_ready')
    async def ready(self):
        print(f'{self.bot.user} logado (v4)')
        await dashboard(self.bot)

def setup(bot):
    bot.add_cog(Ready(bot))