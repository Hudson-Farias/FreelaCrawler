from asyncio import get_event_loop, create_task, gather
from httpx import AsyncClient
from importlib import import_module
from os import listdir
from datetime import time

from database.researches import ResearchesORM
from models.job import Job
from scrapers import get_jobs
from utils.json import json_creater


async def main():
    researches = await ResearchesORM.find_many()

    tasks = []
    async with AsyncClient() as client:
        for file in listdir('scrapers/freelancers'):
            if not file.startswith('_'):
                module = import_module(f'scrapers.freelancers.{file}'.replace('.py', '').replace('/', '.'))

                tasks += [create_task(module.Scraper.run(client, research.search, research.channel_id)) 
                        for research in researches]
        await gather(*tasks)
    
    data = [job.model_dump() for job in get_jobs('freelancer')]
    json_creater(data, 'output.json')
    print('Done')

loop = get_event_loop()
try:
    loop.create_task(main())
    loop.run_forever()
finally: loop.close()