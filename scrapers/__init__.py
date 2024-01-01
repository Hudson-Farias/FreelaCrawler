from abc import ABC, abstractmethod
from httpx import AsyncClient
from asyncio import create_task, gather

from utils.json import json_creater

class Crawler(ABC):
    url = ''
    platform = ''

    page_text = ''

    urls = []
    data = []
    page = 1

    @classmethod
    async def run(cls, *args, **kwargs):
        if not cls.url: raise NotImplementedError('Unspecified url')
        if not cls.platform: raise NotImplementedError('Unspecified platform')

        cls.data = []
        cls.page = 1

        isLastPage = False
        while not isLastPage:
            try: isLastPage = await cls._scraping(cls, *args, **kwargs)
            except Exception as e:
                with open(f'log/html/{cls.platform}-{cls.page}.html', 'w+', encoding = 'utf-8') as file: file.write(response.text)
                break
        
        return cls.data


    @abstractmethod
    async def _scraping(cls, *args, **kwargs): pass

    
    async def request(cls, client: AsyncClient, path_url: str):
        response = await client.get(cls.url + path_url, timeout = 600)
        cls.page_text = response.text        
        cls.page += 1
        return response

    
    def json(cls): json_creater(cls.data, f'log/json/{cls.platform}.json')
