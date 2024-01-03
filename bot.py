from discord import Intents
from discord.ext.commands import Bot

from playwright.async_api import async_playwright
from dotenv import load_dotenv
from os import getenv, listdir

load_dotenv()

client = Bot(intents = Intents.all())

def cogs(path = 'cogs'):
    for file in listdir(path):
        if file != '__pycache__':
            if file.endswith('.py'):
                file = f'{path}.{file}'.replace('.py', '')
                client.load_extension(file.replace('/', '.'))

            else:
                cogs(path + '/' + file)
                
if __name__ == '__main__':
    cogs()
    client.run(getenv('DISCORD_BOT_TOKEN'))