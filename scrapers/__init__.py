from abc import ABC, abstractmethod
from httpx import AsyncClient
from asyncio import create_task, gather
from typing import Union, List, Literal
from models.job import Job
from utils.json import json_creater, json_load

from datetime import datetime
from os.path import exists
from os import makedirs, getenv
from dotenv import load_dotenv

load_dotenv()

urls = []
data: List[Job] = {
    'freelancer': [],
    'fulltime': [],
}

use = getenv('USE')
ended = {
    'freelancer': False,
    'fulltime': False,
}

class Crawler(ABC):
    url = ''
    platform = ''

    search = ''
    page_text = ''

    @classmethod
    async def run(cls, *args, **kwargs):
        if not cls.url: raise NotImplementedError('Unspecified url')
        if not cls.platform: raise NotImplementedError('Unspecified platform')
        
        await cls._scraping(cls, *args, **kwargs)


    @abstractmethod
    async def _scraping(cls, *args, **kwargs): pass

    
    async def request(cls, client: AsyncClient, path_url: str, search: str = ''):
        response = await client.get(cls.url + path_url, timeout = 600)
        cls.page_text = response.text
        cls.search = search
        cls.html(cls)

        return response


    def add_work(cls, job: Union[Job, dict], type: Literal['freelancer', 'fulltime']):
        if isinstance(job, dict): job = Job(**job)

        if job.link in urls: return
        urls.append(job.link)
        data[type].append(job)


    def html(cls):
        path = f'log/html/{cls.platform}'
        if not exists(path): makedirs(path)

        with open(f'{path}/{cls.search}.html', 'w+', encoding = 'utf-8') as file: 
            file.write(cls.page_text)

    
    def json(cls):
        data = [job.dict() for job in cls.data]
        json_creater(data, f'log/json/{cls.platform}.json')


    def last_used():
        if use != 'local': return 1

        timestamp = json_load('log.json')['timestamp']
        now = datetime.now()
        date_timestamp = datetime.fromtimestamp(timestamp)

        difference = now - date_timestamp

        return difference.days


def get_jobs(type: Literal['freelancer', 'fulltime']):
    if use == 'local':
        ended[type] = True

        if ended['fulltime'] and ended['freelancer']:
            now = datetime.now()
            json_creater({'timestamp': int(now.timestamp())}, 'log.json')

    return data[type]