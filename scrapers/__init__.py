from abc import ABC, abstractmethod
from httpx import AsyncClient
from asyncio import create_task, gather
from typing import Union, List
from models.job import Job
from utils.json import json_creater

class Crawler(ABC):
    url = ''
    platform = ''

    page_text = ''

    urls = []

    @classmethod
    async def run(cls, *args, **kwargs):
        if not cls.url: raise NotImplementedError('Unspecified url')
        if not cls.platform: raise NotImplementedError('Unspecified platform')

        cls.data: List[Job] = []
        cls.page = 1
        
        await cls._scraping(cls, *args, **kwargs)
        return cls.data
        
        isLastPage = False
        while not isLastPage:
            try: isLastPage = await cls._scraping(cls, *args, **kwargs)
            except Exception as e:
                with open(f'log/html/{cls.platform}-{cls.page}.html', 'w+', encoding = 'utf-8') as file: file.write(cls.page_text)
                print(e)
                print(type(e))
                break
        return cls.data


    @abstractmethod
    async def _scraping(cls, *args, **kwargs): pass

    
    async def request(cls, client: AsyncClient, path_url: str):
        response = await client.get(cls.url + path_url, timeout = 600)
        cls.page_text = response.text        
        cls.page += 1
        return response


    def add_work(cls, job: Union[Job, dict]):
        if isinstance(job, dict): job = Job(**job)

        if job.link in cls.urls: return
        cls.urls.append(job.link)
        cls.data.append(job)

    
    def json(cls):
        data = [job.dict() for job in cls.data]
        json_creater(data, f'log/json/{cls.platform}.json')
