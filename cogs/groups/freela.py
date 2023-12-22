from discord import Client, SlashCommandGroup, Interaction, Option
from discord.ext.commands import Cog
from discord.abc import GuildChannel

from database.researches import ResearchesORM
from utils.dashboard import dashboard

class Freela(Cog):
    group = SlashCommandGroup('freela', 'Comandos Freela')
    
    def __init__(self, bot: Client):
        self.bot = bot

    @group.command()
    async def add(self, inter: Interaction, search: str, channel: Option(GuildChannel, required = False)):
        channel = channel or inter.channel
        message = f'{channel.mention} não pertence à ***<#1186769104359669852>***'

        if channel.category.id == 1186769104359669852:
            message = f'Pesquisa "***{search}***" foi adicionada a lista'
            await ResearchesORM.create(search = search, channel_id = channel.id)
            await dashboard(self.bot)

        await inter.response.send_message(message, ephemeral = True)
    
def setup(bot):
    bot.add_cog(Freela(bot))