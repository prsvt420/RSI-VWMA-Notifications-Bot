import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')
DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite3'
API_URL = 'https://api.binance.com/api/v3/klines'
