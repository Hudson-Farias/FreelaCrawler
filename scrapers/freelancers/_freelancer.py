from scrapers import Crawler

from httpx import AsyncClient
from bs4 import BeautifulSoup
from re import search

class Scraper(Crawler):
    url = 'https://www.freelancer.com'
    platform = 'freelancer'


    async def _scraping(cls, client: AsyncClient, _search: str, channel_id: int):
        path = '/jobs' if cls.page == 1 else f'/jobs/{cls.page}'
        response = await cls.request(cls, client, f'{path}?keyword={_search}')

        print(f'{cls.url}{path}?keyword={_search}')

        soup = BeautifulSoup(response.text, 'html.parser')
        projects = soup.find_all('div', class_ = 'JobSearchCard-item')

        for project in projects:
            payload = {}

            element = project.find('a', class_ = 'JobSearchCard-primary-heading-link')

            payload['title'] = element.text.strip()
            payload['link'] = cls.url + element.get('href')

            # timestamp = int(int(project.find('b', class_ = 'datetime').get('cp-datetime')) / 1000)
            # payload['description'] = f'**Publicado**: <t:{timestamp}:R>\n'

            bids_element = project.find('div', class_ = 'JobSearchCard-secondary-entry')
            if not bids_element: continue
            payload['description'] = '**Propostas**: ' + bids_element.text.replace(' bids', '')

            payload['footer'] = cls.platform

            payload['icon'] = soup.find('link', rel='icon').get('href')
            payload['channel_id'] = channel_id
            
            if payload['link'] in cls.urls: continue

            cls.data.append(payload)
            cls.urls.append(payload['link'])

        pagination = soup.find('div', id = 'bottom-pagination')

        active = pagination.find('a', class_ = 'is-active')
        pages = [e for e in pagination.find_all('a') if e.text.isdigit()]

        isLastPage = active.text == pages[-1].text
        return isLastPage
