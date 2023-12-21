from dotenv import load_dotenv
from os import getenv

load_dotenv()

PROTOCOL = getenv('PROTOCOL')
CONNECTOR = getenv('CONNECTOR_SYNC')
PROTOCOL = getenv('PROTOCOL')
USERNAME = getenv('DB_USERNAME')
PASSWORD = getenv('DB_PASSWORD')
HOST = getenv('DB_HOST')
DB = getenv('DB_NAME')

SQL_URL =  f'{PROTOCOL}{CONNECTOR}://'

if USERNAME and PASSWORD: SQL_URL += f'{USERNAME}:{PASSWORD}@'

SQL_URL += f'{HOST}'

if DB: SQL_URL += f'/{DB}'

with open('alembic.example', 'r', encoding = 'UTF-8') as file:
    text = file.read().replace('{DB_URL}', SQL_URL)
    
    with open('alembic.ini', 'w+', encoding = 'UTF-8') as file:
        file.write(text)