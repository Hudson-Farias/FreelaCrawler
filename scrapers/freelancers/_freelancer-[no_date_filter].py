from scrapers import Crawler

from httpx import AsyncClient
from bs4 import BeautifulSoup
from re import search

from models.job import Job

class Scraper(Crawler):
    url = 'https://www.freelancer.com'
    platform = 'Freelancer'


    async def _scraping(cls, client: AsyncClient, _search: str, channel_id: int, _page: int = 1):
        path = '/jobs' if _page == 1 else f'/jobs/{_page}'
        response = await cls.request(cls, client, f'{path}?keyword={_search}')

        soup = BeautifulSoup(response.text, 'html.parser')
        projects = soup.find_all('div', class_ = 'JobSearchCard-item')

        for project in projects:
            job = Job()

            element = project.find('a', class_ = 'JobSearchCard-primary-heading-link')

            job.title = element.text.strip()
            job.link = cls.url + element.get('href')

            bids_element = project.find('div', class_ = 'JobSearchCard-secondary-entry')
            if not bids_element: continue
            job.description = '**Propostas**: ' + bids_element.text.replace(' bids', '')

            job.footer = cls.platform

            job.icon = soup.find('link', rel='icon').get('href')
            job.channel_id = channel_id

            cls.add_work(cls, job, 'freelancer')

        pagination = soup.find('div', id = 'bottom-pagination')

        active = pagination.find('a', class_ = 'is-active')
        pages = [e for e in pagination.find_all('a') if e.text.isdigit()]

        if active.text != pages[-1].text:
            print(f'[{cls.platform}] {search}: {_page}')
            await _scraping(cls, client, _search, channel_id, _page + 1)
