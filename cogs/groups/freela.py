from discord import Client, SlashCommandGroup, Interaction, Option
from discord.ext.commands import Cog
from discord.abc import GuildChannel

from database.freelancers import FreelancersORM
from utils.dashboard import dashboard

class Freela(Cog):
    group = SlashCommandGroup('freela', 'Comandos Freela')
    
    def __init__(self, bot: Client):
        self.bot = bot

    @group.command()
    async def add(self, inter: Interaction, search: str, channel: Option(GuildChannel, required = False)):
        channel = channel or inter.channel

        message = f'Pesquisa "***{search}***" foi adicionada a lista'
        await FreelancersORM.create(search = search, channel_id = channel.id)
        await dashboard(self.bot)
        await inter.channel.send(message)
    
def setup(bot):
    bot.add_cog(Freela(bot))