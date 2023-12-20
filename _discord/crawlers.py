from discord import Client, Embed
from discord.ext.commands import Cog
from discord.ext.tasks import loop

from asyncio import create_task, gather
from httpx import AsyncClient
from datetime import time

from scrapers.workana import Scraper
from utils.json import json_load

researches = json_load('researches.json')

times = [
    time(10, 0, 0)
    # , time(16, 9, 30)
]

class Crawlling(Cog):
    def __init__(self, bot: Client):
        self.bot = bot
        
        
    @Cog.listener('on_ready')
    async def ready(self):
        self.crawler.start()
        print('Loop: Crawler iniciado')


    @loop(time = times)
    async def crawler(self):
        data = []
        async with AsyncClient() as client:
            for research in researches:
                data += await Scraper.run(client, research['search'], research['channel_id'])
            
        tasks = [create_task(self.sender_embed(i)) for i in data]
        await gather(*tasks)


    async def sender_embed(self, payload):
        channel = self.bot.get_channel(payload['channel_id'])
        embed = Embed()

        embed.title = payload['title']
        embed.url = payload['link']
        embed.description = payload['description'][:4096]
        embed.set_footer(text = payload['footer'], icon_url = payload['icon'])

        await channel.send(embed = embed)


def setup(bot):
    bot.add_cog(Crawlling(bot))