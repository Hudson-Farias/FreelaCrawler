from playwright.async_api import async_playwright
from httpx import AsyncClient
from bs4 import BeautifulSoup
from asyncio import run
from os import getenv
from dotenv import load_dotenv

# from scrapers.freelancers._freelancer import Scraper
from scrapers.freelancers.nnfreelas import Scraper
# from scrapers.freelancers.workana import Scraper

# from scrapers.fulltime.catho import Scraper
# from scrapers.fulltime.linkedin import Scraper

load_dotenv()

search = 'Python'

async def main():
    async with async_playwright() as p:
        async with AsyncClient() as client:
            browser = await p.chromium.launch(headless = True)
            # browser = await p.chromium.launch(headless = getenv('HEADLESS') == 'true')

            params = {
                'page': await browser.new_page(), 
                'client': client, 
                'search': search, 
                'channel_id': 1,
                '_page': 1
            }

            await Scraper.run(**params)
            await browser.close()

run(main())
