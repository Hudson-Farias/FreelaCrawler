from discord import Client, Embed
from discord.ext.commands import Cog
from discord.ext.tasks import loop

from asyncio import create_task, gather
from httpx import AsyncClient
from datetime import datetime, timedelta, time
from importlib import import_module
from os import listdir

from database.researches import ResearchesORM

now = datetime.now()

times = [
    (now + timedelta(hours = 3, seconds = 10) - timedelta(microseconds = now.microsecond)).time(),
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

        tasks = [self.delete_messages(research.channel_id) for research in researches]
        await gather(*tasks)

        tasks = []
        async with AsyncClient() as client:
            for file in listdir('scrapers'):
                if not file.startswith('_'):
                    module = import_module(f'scrapers.{file}'.replace('.py', '').replace('/', '.'))
                    tasks += [create_task(module.Scraper.run(client, research.search, research.channel_id)) 
                            for research in researches]

            results = await gather(*tasks)
        
        # data = []
        # for i in results: data += i
            
        # tasks = [create_task(self.sender_embed(i)) for i in data]
        # await gather(*tasks)
        # print('='*30)


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


    async def delete_messages(self, channel_id):
        channel = self.bot.get_channel(channel_id)
        await channel.purge(limit = 1000)
        

def setup(bot):
    bot.add_cog(Crawlling(bot))
