from discord import Client, slash_command, Interaction, Option
from discord.ext.commands import Cog, has_guild_permissions
from discord.abc import GuildChannel

class Clear(Cog):
    def __init__(self, bot: Client):
        self.bot = bot

    @slash_command()
    @has_guild_permissions(manage_messages = True)
    async def clear(self, inter: Interaction, amount: Option(int, default = 30), channel: Option(GuildChannel, required = False)):
        msg = f'Apagando {amount} mensagens'
        await inter.response.send_message(msg, ephemeral = True)
        channel = channel or inter.channel

        await channel.purge(limit = amount)

def setup(bot):
    bot.add_cog(Clear(bot))