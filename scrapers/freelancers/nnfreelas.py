from scrapers import Crawler

from httpx import AsyncClient
from bs4 import BeautifulSoup
from re import findall

from models.job import Job

class Scraper(Crawler):
    url = 'https://www.99freelas.com.br'
    platform = '99freelas'


    async def _scraping(cls, client: AsyncClient, search: str, channel_id: int, _page: int = 1, **_):
        path = f'/projects?q={_search}&page={_page}'

        last_day = '&data-da-publicacao=menos-de-24-horas-atras'
        last_2days = '&data-da-publicacao=menos-de-3-dias-atras'

        days = cls.last_used()
        path +=  last_day if  days <= 1 else (last_2days if days <= 3 else '')

        response = await cls.request(cls, client, f'/projects?q={_search}&page={_page}', _search)

        soup = BeautifulSoup(response.text, 'html.parser')
        projects = soup.find_all('li', class_ = 'result-item')

        for project in projects:
            job = Job()

            element = project.find('h1', class_ = 'title')

            job.title = element.text.strip()
            if 'aposta' in job.title.lower(): continue

            job.link = cls.url + element.find('a').get('href').strip().replace(f'?ref=projects_{_page}', '')

            timestamp = int(int(project.find('b', class_ = 'datetime').get('cp-datetime')) / 1000)
            job.description = f'**Publicado**: <t:{timestamp}:R>\n'

            bids_element = project.find('p', class_ = 'item-text')

            job.description += '**Propostas**: ' + findall(r'Propostas: (\d+)', bids_element.text)[0]

            job.footer = cls.platform

            job.icon = soup.find('link', rel='icon').get('href')
            job.channel_id = channel_id

            cls.add_work(cls, job, 'freelancer')

        pagination = soup.find('div', class_ = 'pagination-component')
        if not pagination: return

        active = pagination.find('span', class_ = 'selected')
        pages = pagination.find_all('span')

        if active.text != pages[-1].text:
            await cls._scraping(cls, client, _search, channel_id, _page + 1)
