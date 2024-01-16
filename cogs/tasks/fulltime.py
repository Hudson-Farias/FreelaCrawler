from discord import Client, Embed
from discord.ext.commands import Cog
from discord.ext.tasks import loop

from asyncio import create_task, gather
from playwright.async_api import async_playwright
from httpx import AsyncClient
from importlib import import_module
from os import getenv, listdir
from datetime import time
from dotenv import load_dotenv

from models.job import Job
from scrapers import get_jobs

load_dotenv()

class Fulltime(Cog):
    def __init__(self, bot: Client):
        self.bot = bot


    @Cog.listener('on_ready')
    async def ready(self):
        await self.crawling()
        self.crawler.start()


    @loop(time = time(10, 0, 0))
    async def crawler(self):
        await self.crawling()
        

    async def crawling(self):
        print('[Fulltime] running')
        channels_id = [1165659662599852103, 1165659721299136532]

        tasks = [self.delete_messages(channel_id) for channel_id in channels_id]
        await gather(*tasks)

        tasks = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless = getenv('HEADLESS') == 'true')

            async with AsyncClient() as client:
                for file in listdir('scrapers/fulltime'):
                    if not file.startswith('_'):
                        params = {}
                        params['client'] = client

                        module = import_module(f'scrapers.fulltime.{file}'.replace('.py', '').replace('/', '.'))

                        params['page'] = await browser.new_page()
                        params['channel_id'] = 1165659662599852103
                        params['is_remote'] = True
                        tasks.append(create_task(module.Scraper.run(**params)))
                        
                        params['page'] = await browser.new_page()
                        params['channel_id'] = 1165659721299136532
                        params['is_remote'] = False
                        tasks.append(create_task(module.Scraper.run(**params)))

                        await gather(*tasks)
        
        tasks = [create_task(self.sender_embed(i)) for i in get_jobs('fulltime')]
        await gather(*tasks)
        print('[Fulltime] ending')


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
    bot.add_cog(Fulltime(bot))

