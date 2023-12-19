from abc import ABC, abstractmethod

class Crawler(ABC):
    @classmethod
    @abstractmethod
    async def run(cls):
        pass