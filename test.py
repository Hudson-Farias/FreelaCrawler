from playwright.async_api import async_playwright
from httpx import AsyncClient
from bs4 import BeautifulSoup
from asyncio import run

# from scrapers.freelancers.freelancer import Scraper
# from scrapers.freelancers.nnfreelas import Scraper
# from scrapers.freelancers.workana import Scraper

from scrapers.fulltime.linkedin import Scraper

async def main():
    async with async_playwright() as p:
        async with AsyncClient() as client:
            browser = await p.chromium.launch(headless = False)
            
            page = await browser.new_page()
            data = await Scraper.run(page, client, 'Python', 1)
            print(len(data))
            input('Enter...')
            await browser.close()

    # async with AsyncClient() as client:
    #     data = await Scraper.run(client, 'landing page', 1)
    #     print(len(data))

run(main())