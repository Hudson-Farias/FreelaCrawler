from asyncio import run, get_event_loop, create_task, gather
from playwright.async_api import async_playwright
from httpx import AsyncClient
from importlib import import_module
from os import getenv, listdir
from dotenv import load_dotenv
from datetime import time

from database.freelancers import FreelancersORM
from models.job import Job
from scrapers import get_jobs
from utils.json import json_creater

load_dotenv()

async def main():
    researches = await FreelancersORM.find_many()

    tasks = []
    async with async_playwright() as p:
        async with AsyncClient() as client:
            for file in listdir('scrapers/freelancers'):
                if not file.startswith('_'):
                    module = import_module(f'scrapers.freelancers.{file}'.replace('.py', '').replace('/', '.'))

                    tasks += [create_task(module.Scraper.run(client, research.search, research.channel_id)) 
                            for research in researches]


            browser = await p.chromium.launch(headless = getenv('HEADLESS') == 'true')

            for file in listdir('scrapers/fulltime'):
                if not file.startswith('_'):
                    params = {}
                    params['client'] = client

                    module = import_module(f'scrapers.fulltime.{file}'.replace('.py', '').replace('/', '.'))

                    params['page'] = await browser.new_page()
                    params['channel_id'] = 0
                    params['is_remote'] = True
                    tasks.append(create_task(module.Scraper.run(**params)))
                    
                    params['page'] = await browser.new_page()
                    params['channel_id'] = 0
                    params['is_remote'] = False
                    tasks.append(create_task(module.Scraper.run(**params)))

            await gather(*tasks)
    
    data = [job.model_dump() for job in get_jobs('freelancer')]
    json_creater(data, 'output.json')
    print('Done')


run(main())

# loop = get_event_loop()
# try:
#     loop.create_task(main())
#     loop.run_forever()
# finally: loop.close()