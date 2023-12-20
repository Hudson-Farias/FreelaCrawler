from discord import Client, Embed, Colour
from discord.ext.commands import Cog

from asyncio import run, create_task, gather
from httpx import AsyncClient

from scrapers.workana import Scraper

from utils.json import json_load, json_creater

researches = json_load('researches.json')

class Crawler(Cog):
    def __init__(self, bot: Client):
        self.bot = bot

    @Cog.listener('on_ready')
    async def crawler(self):
        data = []
        async with AsyncClient() as client:
            for research in researches:
                data += await Scraper.run(client, research['search'], research['channel_id'])
                # break
            
        # json_creater(data, f'data.json')
        # tasks = [create_task(self.sender_embed(i)) for i in data]
        # await gather(*tasks)
        # print('acabo')


    async def sender_embed(self, payload):
        channel = self.bot.get_channel(payload['channel_id'])
        embed = Embed()

        embed.title = payload['title']
        embed.url = payload['link']
        embed.description = payload['description'][:4096]
        embed.set_footer(text = payload['footer'], icon_url = payload['icon'])

        await channel.send(embed = embed)


def setup(bot):
    bot.add_cog(Crawler(bot))