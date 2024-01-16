from scrapers import Crawler

from playwright.async_api._generated import Page, ElementHandle
from httpx import AsyncClient
from bs4 import BeautifulSoup
from asyncio import sleep
from re import findall, escape, IGNORECASE

from models.job import Job

tools = [
    'react', 
    'python', 
    'typescript', 
    'next', 
    'fastapi', 
    'selenium', 
    'webscraping', 
    'playwright'
]

class Scraper(Crawler):
    url = 'https://www.linkedin.com'
    platform = 'Linkedin'

    blacklist = ['GeekHunter', 'Netvagas', 'BNE - Banco Nacional de Empregos']
    scroll_position = 0

    @staticmethod
    async def _scraping(cls, page: Page, client: AsyncClient, channel_id: int, is_remote: bool = True):
        # search = '("RPA") AND ("Python")'
        search = '("Desenvolvedor" OR "Programador") AND ("Pleno" OR "PL") AND ("Python" OR "Typescript" OR "Javascript")'
        
        url = f'{cls.url}/jobs/search/?location=Brasil&geoId=106057199&keywords={search}'
        last_day = '&f_TPR=r86400'
        last_week = '&f_TPR=r604800'

        url +=  last_day if cls.last_used() == 1 else last_week
        
        if is_remote: url += '&f_WT=2'
        else: 
            url += '&f_PP=106701406' # RJ
            url += '&f_WT=1%2C3' # presencial e híbrido
        
        await page.goto(url)
        await cls.__scroll(cls, page)
        print('[Linkedin] scroll ending')

        jobs = await page.query_selector_all('.jobs-search__results-list li')

        for i, job in enumerate(jobs):            
            company_name = await cls.__get_selector_inner_text(page, '.base-search-card__subtitle', job)
            if company_name in cls.blacklist: continue
            
            url  = await (await job.query_selector('a')).get_attribute('href')

            response = await cls.__request_job_infos(cls, client, url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            payload = Job()
            payload.title = soup.find('h1', class_ = 'top-card-layout__title').text.strip()
            print(f'[Linkedin] {payload.title}')
            payload.link = url
            payload.description = soup.find('div', class_ = 'show-more-less-html__markup').text.strip()

            payload.icon = soup.find('link', rel='icon').get('href')
            payload.footer = company_name
            payload.channel_id = channel_id
            
            text = payload.title  + '\n' + payload.description
            pattern = '|'.join(escape(s) for s in tools)
            requirements = findall(pattern, text, IGNORECASE)

            payload.description = ''
            if requirements: cls.add_work(cls, payload, 'fulltime')

        print('[Linkedin] loop ending')


    async def __request_job_infos(cls, client: AsyncClient, url: str):
        response = await client.get(url, timeout = 600)
        if not 'body' in response.text: return await cls.__request_job_infos(cls, client, url)

        cls.page_text = response.text
        return response


    async def __scroll(cls, page: Page):
        more = page.locator('.infinite-scroller__show-more-button')

        if (await more.is_visible()): await more.click()

        await page.locator('body').evaluate('e => scroll(0, e.scrollHeight)')
        await sleep(2)
        scroll_position = await page.evaluate('e => pageYOffset')
        
        if cls.scroll_position != scroll_position:
            cls.scroll_position = scroll_position
            
            return await cls.__scroll(cls, page)


    async def __get_selector_inner_text(page: Page, selector: str, element_handle: ElementHandle | None = None):
        if not element_handle: return (await page.inner_text(selector)).strip()

        element = await element_handle.query_selector(selector)
        return (await element.inner_text()).strip()