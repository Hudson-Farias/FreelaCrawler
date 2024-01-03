from scrapers import Crawler

from httpx import AsyncClient
from bs4 import BeautifulSoup
from re import search

class Scraper(Crawler):
    url = 'https://www.99freelas.com.br'
    platform = '99freelas'


    async def _scraping(cls, client: AsyncClient, _search: str, channel_id: int):
        response = await cls.request(cls, client, f'/projects?q={_search}&page={cls.page}')

        soup = BeautifulSoup(response.text, 'html.parser')
        projects = soup.find_all('li', class_ = 'result-item')

        for project in projects:
            payload = {}

            element = project.find('h1', class_ = 'title')

            payload['title'] = element.text.strip()
            payload['link'] = cls.url + element.find('a').get('href').strip().replace(f'?ref=projects_{cls.page}', '')

            timestamp = int(int(project.find('b', class_ = 'datetime').get('cp-datetime')) / 1000)
            payload['description'] = f'**Publicado**: <t:{timestamp}:R>\n'

            bids_element = project.find('p', class_ = 'item-text')
            payload['description'] += '**Propostas**: ' + search(r'Propostas: (\d+)', bids_element.text).group(1)

            payload['footer'] = '99freelas'

            payload['icon'] = soup.find('link', rel='icon').get('href')
            payload['channel_id'] = channel_id
            
            if payload['link'] in cls.urls: continue

            cls.data.append(payload)
            cls.urls.append(payload['link'])

        pagination = soup.find('div', class_ = 'pagination-component')
        if not pagination: return cls.data

        active = pagination.find('span', class_ = 'selected')
        pages = pagination.find_all('span')

        isLastPage = active.text == pages[-1].text
        return isLastPage