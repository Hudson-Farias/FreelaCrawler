from discord import Client, Intents, Embed, Colour

from playwright.async_api import async_playwright
from httpx import AsyncClient
from asyncio import run, create_task, gather
from dotenv import load_dotenv
from os import getenv

from scrapers.workana import Scraper

from utils.json import json_load

load_dotenv()

researches = json_load('researches.json')

client = Client(intents = Intents.all())


async def sender_embed(payload):
    channel = client.get_channel(payload['channel_id'])
    embed = Embed()

    embed.title = payload['title']
    embed.url = payload['link']
    embed.description = payload['description']
    embed.set_footer(text = payload['footer'], icon_url = payload['icon'])

    await channel.send(embed = embed)


@client.event
async def on_ready():
    print(f'{client.user} logado')
    data = []

    async with AsyncClient() as client_httpx:
        for research in researches:
            data += await Scraper.run(client_httpx, research['search'], research['channel_id'])
            break
    
    tasks = [create_task(sender_embed(i)) for i in data]
    await gather(*tasks)

client.run(getenv('DISCORD_TOKEN'))