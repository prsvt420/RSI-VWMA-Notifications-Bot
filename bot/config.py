import logging
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')
DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite3'
API_URL = 'https://api.binance.com/api/v3/klines'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('logs/bot.log')]
)
