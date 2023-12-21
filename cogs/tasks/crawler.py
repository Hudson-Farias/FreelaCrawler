from discord import Client, Embed
from discord.ext.commands import Cog
from discord.ext.tasks import loop

from asyncio import create_task, gather
from httpx import AsyncClient
from datetime import datetime, timedelta, time

from scrapers.workana import Scraper
from database.researches import ResearchesORM

now = datetime.now()

times = [
    # (now + timedelta(hours = 3, seconds = 15) - timedelta(microseconds = now.microsecond)).time(),
    time(10, 0, 0)
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
        print('rodando')
        researches = await ResearchesORM.find_many()

        async with AsyncClient() as client:
            tasks = [create_task(Scraper.run(client, research.search, research.channel_id)) 
                        for research in researches]

            results = await gather(*tasks)
        
        data = []
        for i in results: data += i
            
        tasks = [create_task(self.sender_embed(i)) for i in data]
        await gather(*tasks)


    async def sender_embed(self, payload):
        channel = self.bot.get_channel(payload['channel_id'])
        embed = Embed()

        embed.title = payload['title']
        embed.url = payload['link']
        embed.description = 'ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ'
        embed.description += payload['description']
        embed.description += 'ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ'
        embed.set_footer(text = payload['footer'], icon_url = payload['icon'])

        await channel.send(embed = embed)


def setup(bot):
    bot.add_cog(Crawlling(bot))