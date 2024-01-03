from playwright.async_api import async_playwright
from httpx import AsyncClient
from bs4 import BeautifulSoup
from asyncio import run

# from scrapers.freelancers._freelancer import Scraper
# from scrapers.freelancers.nnfreelas import Scraper
# from scrapers.freelancers.workana import Scraper

from scrapers.fulltime.linkedin import Scraper

search = 'Python'

async def main():
    async with async_playwright() as p:
        async with AsyncClient() as client:
            browser = await p.chromium.launch(headless = False)

            params = {
                'page': await browser.new_page(), 
                'client': client, 
                'search': search, 
                'channel_id': 1
            }
            data = await Scraper.run(**params)
            print(len(data))
            input('Enter...')

            await browser.close()

run(main())