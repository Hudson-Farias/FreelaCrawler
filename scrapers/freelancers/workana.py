from scrapers import Crawler

from httpx import AsyncClient
from bs4 import BeautifulSoup
from datetime import datetime

from models.job import Job

mounths = {
    'janeiro': 'January',
    'fevereiro': 'February',
    'março': 'March',
    'abril': 'April',
    'maio': 'May',
    'junho': 'June',
    'julho': 'July',
    'agosto': 'August',
    'setembro': 'September',
    'outubro': 'October',
    'novembro': 'November',
    'dezembro': 'December'
}

def translate(date: str):
    for pt, en in mounths.items():
        date = date.replace(pt, en)

    return date

class Scraper(Crawler):
    url = 'https://www.workana.com'
    platform = 'Workana'


    @staticmethod
    async def _scraping(cls, client: AsyncClient, search: str, channel_id: int, _page: int = 1):
        response = await cls.request(cls, client, f'/pt/jobs?category=it-programming&language=pt&query={search}&page={_page}&publication=1w', search)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        projects = soup.find_all('div', class_ = 'project-item')

        if not projects: return

        for project in projects:
            job = Job()

            element = project.find('h2', class_ = 'project-title')

            job.title = element.text.strip()
            job.link = cls.url + element.find('a').get('href').strip().replace(f'?ref=projects_{_page}', '')
            
            time = project.find('span', class_ = 'date').get('title').lower()
            time = translate(time)
            timestamp = int(datetime.strptime(time, '%d de %B de %Y %H:%M').timestamp())
            job.description = f'**Publicado**: <t:{timestamp}:R>\n'

            job.description += '**Propostas**: ' + project.find('span', class_ = 'bids').text.strip().replace('Propostas: ', '') + '\n'

            job.footer = f'{cls.platform}: ' + project.find('span', class_ = 'values').text.strip()

            job.icon = soup.find('link', rel='icon').get('href')
            job.channel_id = channel_id
        
            cls.add_work(cls, job, 'freelancer')

        pagination = soup.find('ul', class_ = 'pagination')
        active = pagination.find('li', 'active')
        pages = pagination.find_all('li')

        if not active:
            print(f'[{cls.platform}] {search}: {_page}')
            return
            
        if active.text != pages[-1].text:
            print(f'[{cls.platform}] {search}: {_page}')
            await cls._scraping(cls, client, search, channel_id, _page +1)