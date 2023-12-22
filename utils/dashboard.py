from discord import Client, Embed

from database.researches import ResearchesORM

async def dashboard(bot: Client):
    researches = await ResearchesORM.find_many()
    channel = await bot.fetch_channel(1187539924195483779)
    message = await channel.fetch_message(1187540417420476578)

    channels = {}

    for research in researches:
        if research.channel_id not in channels: channels[research.channel_id] = ''
        channels[research.channel_id] += research.search + ', '

    embed = Embed()
    embed.description = ''

    for channel_id, searches in channels.items():
        channel = bot.get_channel(channel_id)
        embed.description += f'**{channel.name.capitalize().replace("-", " ")}**: {searches.strip(", ")}\n'

    await message.edit('', embed = embed)