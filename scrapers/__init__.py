from abc import ABC, abstractmethod

class Crawler(ABC):
    @classmethod
    async def run(cls, *args, **kwargs):
        data = await cls._scraping(cls, *args, **kwargs, page = 1, data = [])
        return data


    @abstractmethod
    async def _scraping(cls, *args, **kwargs): pass