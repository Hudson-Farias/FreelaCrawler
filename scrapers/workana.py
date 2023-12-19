from scrapers import Crawler

from httpx import AsyncClient
from bs4 import BeautifulSoup

class Scraper(Crawler):
    url_base = 'https://www.workana.com'


    @classmethod
    async def run(cls, client: AsyncClient, search: str, channel_id: int):
        page = 1
        data = []
        data += await cls.__scraping(cls, client, search, page, channel_id)

        return data


    async def __scraping(cls, client: AsyncClient, search: str, page: int, channel_id: int, data: list = []):
        response = await client.get(f'{cls.url_base}/pt/jobs?category=it-programming&language=pt&query={search}&page={page}', timeout = 600)
        soup = BeautifulSoup(response.text, 'html.parser')

        projects = soup.find_all('div', class_ = 'project-item')

        for project in projects:
            payload = {}

            element = project.find('h2', class_ = 'project-title')

            payload['title'] = element.text.strip()
            payload['link'] = cls.url_base + element.find('a').get('href').strip()
            
            payload['description'] = project.find('div', class_ = 'project-details').text.strip()

            payload['footer'] = 'Workana: ' + project.find('span', class_ = 'values').text.strip()

            payload['icon'] = soup.find('link', rel='icon').get('href')
            payload['channel_id'] = channel_id
            
            data.append(payload)

            return data

        pagination = soup.find('ul', class_ = 'pagination')
        active = pagination.find('li', 'active')
        pages = pagination.find_all('li')
        return data if active.text == pages[-1].text else await cls.__scraping(cls, client, search, page + 1, channel_id, data)
