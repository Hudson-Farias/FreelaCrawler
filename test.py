from httpx import AsyncClient
from bs4 import BeautifulSoup
from asyncio import run

# from scrapers.nnfreelas import Scraper
from scrapers.workana import Scraper

async def main():
    async with AsyncClient() as client:
        data = await Scraper.run(client, 'webscraping', 1)
        print(len(data))

run(main())