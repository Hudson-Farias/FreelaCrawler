from discord import Client, Embed
from discord.ext.commands import Cog
from discord.ext.tasks import loop

from asyncio import create_task, gather
from httpx import AsyncClient
from importlib import import_module
from os import listdir
from datetime import time

from database.researches import ResearchesORM
from models.job import Job
from scrapers import get_jobs

class Crawlling(Cog):
    def __init__(self, bot: Client):
        self.bot = bot


    @Cog.listener('on_ready')
    async def ready(self):
        await self.crawling()

        self.crawler.start()
        print('Loop: Crawler iniciado')


    @loop(time = time(10, 0, 0))
    async def crawler(self):
        await self.crawling()
        

    async def crawling(self):
        print('rodando')
        researches = await ResearchesORM.find_many()

        tasks = [self.delete_messages(research.channel_id) for research in researches]
        await gather(*tasks)

        tasks = []
        async with AsyncClient() as client:
            for file in listdir('scrapers/freelancers'):
                if not file.startswith('_'):
                    print(file)
                    module = import_module(f'scrapers.freelancers.{file}'.replace('.py', '').replace('/', '.'))

                    tasks += [create_task(module.Scraper.run(client, research.search, research.channel_id)) 
                            for research in researches]

            await gather(*tasks)
        
        tasks = [create_task(self.sender_embed(i)) for i in get_jobs('freelancer')]
        await gather(*tasks)
        print('='*30)


    async def sender_embed(self, job: Job):
        channel = self.bot.get_channel(job.channel_id)

        embed = Embed()

        embed.title = job.title
        embed.url = job.link
        embed.description = 'ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ'
        embed.description += job.description
        embed.description += 'ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ'
        embed.set_footer(text = job.footer, icon_url = job.icon)

        await channel.send(embed = embed)


    async def delete_messages(self, channel_id):
        channel = self.bot.get_channel(channel_id)
        await channel.purge(limit = 1000)
        

def setup(bot):
    bot.add_cog(Crawlling(bot))
