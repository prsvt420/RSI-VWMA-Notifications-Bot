import json

import aiohttp

from bot.config import API_URL


async def is_valid_symbol(symbol: str) -> bool:
    url = f'{API_URL}?symbol={symbol}&interval=1m&limit=1'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status == 200
    except aiohttp.client_exceptions.ClientConnectorError:
        return await is_valid_symbol(symbol)


async def is_valid_interval(interval: str) -> bool:
    path: str = 'bot/services/notifications_service/intervals.json'

    with open(path, encoding='utf-8') as json_file:
        valid_intervals = json.load(json_file)
    return interval in valid_intervals['valid_intervals']


async def is_valid_period(period: str) -> bool:
    return period.isdigit() and int(period) > 0


async def get_interval_text(interval: str, language: str) -> str:
    if language not in ['ru', 'en']:
        return 'Язык не найден'

    path: str = 'bot/services/notifications_service/intervals.json'

    with open(path, encoding='utf-8') as json_file:
        valid_intervals = json.load(json_file)
    return valid_intervals[f'intervals_text_{language}'][interval]


async def is_valid_notification_data(notification_data: str) -> str:
    if '-' not in notification_data:
        return 'Неправильный формат, повторите попытку\U00002757'

    symbol, interval = notification_data.split('-')
    symbol, interval = symbol.strip().upper(), interval.strip()

    if not await is_valid_symbol(symbol) and not await is_valid_interval(interval):
        return 'Неправильный символ и интервал, повторите попытку\U00002757'

    if not await is_valid_symbol(symbol):
        return 'Неправильный символ, повторите попытку\U00002757'
    if not await is_valid_interval(interval):
        return 'Неправильный интервал, повторите попытку\U00002757'

    return ''


async def convert_rus_interval_to_en(interval: str) -> str:
    path: str = 'bot/services/notifications_service/intervals.json'

    with open(path, encoding='utf-8') as json_file:
        intervals = json.load(json_file)

    return intervals['intervals_ru'][interval]


async def interval_is_russian(interval: str) -> bool:
    path: str = 'bot/services/notifications_service/intervals.json'

    with open(path, encoding='utf-8') as json_file:
        intervals = json.load(json_file)

    return interval in intervals['intervals_ru']
