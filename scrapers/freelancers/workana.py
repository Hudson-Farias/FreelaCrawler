from scrapers import Crawler

from httpx import AsyncClient
from bs4 import BeautifulSoup
from datetime import datetime

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
    platform = 'workana'

    @staticmethod
    async def _scraping(cls, client: AsyncClient, search: str, channel_id: int):
        response = await cls.request(cls, client, f'/pt/jobs?category=it-programming&language=pt&query={search}&page={cls.page}&publication=1w')
        
        soup = BeautifulSoup(response.text, 'html.parser')
        projects = soup.find_all('div', class_ = 'project-item')

        if not projects: return cls.data

        for project in projects:
            payload = {}

            element = project.find('h2', class_ = 'project-title')

            payload['title'] = element.text.strip()
            payload['link'] = cls.url + element.find('a').get('href').strip().replace(f'?ref=projects_{cls.page}', '')
            

            time = project.find('span', class_ = 'date').get('title').lower()
            time = translate(time)
            timestamp = int(datetime.strptime(time, '%d de %B de %Y %H:%M').timestamp())
            payload['description'] = f'**Publicado**: <t:{timestamp}:R>\n'

            payload['description'] += '**Propostas**: ' + project.find('span', class_ = 'bids').text.strip().replace('Propostas: ', '') + '\n'

            # payload['description'] = project.find('div', class_ = 'project-details').text.strip()

            payload['footer'] = 'Workana: ' + project.find('span', class_ = 'values').text.strip()

            payload['icon'] = soup.find('link', rel='icon').get('href')
            payload['channel_id'] = channel_id
            
            if payload['link'] in cls.urls: continue

            cls.data.append(payload)
            cls.urls.append(payload['link'])

        pagination = soup.find('ul', class_ = 'pagination')
        active = pagination.find('li', 'active')
        pages = pagination.find_all('li')

        isLastPage = isLastPage = active.text == pages[-1].text if active else True
        return isLastPage