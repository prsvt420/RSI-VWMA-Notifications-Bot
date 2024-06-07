from typing import Optional

import numpy as np
import talib
import aiohttp
import asyncio

from aiogram import Bot

from bot.config import API_URL
from bot.database.crud.notifications_crud import select_notifications
from bot.database.crud.users_crud import select_users_by_notification_id
from bot.database.models import Notifications, Users
from bot.utils.notifications_utils import get_interval_text

storage_sent_notifications: set = set()


async def handle_notifications(bot: Bot) -> None:
    while True:
        notifications: list[Notifications] = await select_notifications()

        for notification in notifications:
            users: list[Users] = await select_users_by_notification_id(notification.id)

            if users:
                await send_notification_to_users(bot, users, notification)

        await asyncio.sleep(5)


async def send_notification_to_users(bot: Bot, users: list[Users], notification: Notifications) -> None:
    for user in users:
        user_telegram_id = user.telegram_id
        symbol = notification.symbol
        interval = notification.interval
        rsi_period = notification.rsi_period
        ma_period = notification.ma_period

        klines = await get_klines(symbol, interval, 200)
        close_prices = await get_close_prices(klines)
        volumes = await get_volumes(klines)
        rsi = await get_rsi(close_prices, rsi_period)
        rsi_vwma = await get_rsi_vwma(rsi, volumes, ma_period)
        crossing_status = await check_crossing(rsi, rsi_vwma)

        notification_data = (user_telegram_id, interval, symbol, rsi_period, ma_period, crossing_status)

        if crossing_status and notification_data not in storage_sent_notifications:
            message: str = await create_message(symbol, interval, crossing_status, rsi)
            await send_message_to_user(bot, user_telegram_id, message)
            storage_sent_notifications.add(notification_data)


async def send_message_to_user(bot: Bot, user_telegram_id: int, message: str) -> None:
    try:
        await bot.send_message(user_telegram_id, message, parse_mode='html')
    except Exception as e:
        print(e)


async def get_klines(symbol: str, interval: str, limit: int) -> list[list[str]]:
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL, params=params) as response:
            response_data: dict = await response.json()
            return [[kline[4], kline[5]] for kline in response_data]


async def get_price_symbol(symbol: str) -> str:
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_data: dict = await response.json()
            return response_data['price']


async def get_close_prices(klines: list[list[str]]) -> np.ndarray:
    return np.array([float(kline[0]) for kline in klines], dtype=np.float64)


async def get_volumes(klines: list[list[str]]) -> np.ndarray:
    return np.array([float(kline[1]) for kline in klines], dtype=np.float64)


async def get_rsi(close_prices: np.ndarray, rsi_period: int) -> np.ndarray:
    return talib.RSI(close_prices, timeperiod=rsi_period)


async def get_rsi_vwma(rsi: np.ndarray, volumes: np.ndarray, ma_period: int) -> np.ndarray:
    rsi_vwma = np.full_like(rsi, np.nan)
    for i in range(ma_period - 1, len(rsi)):
        sum_rsi_vol = np.sum(rsi[i - ma_period + 1:i + 1] * volumes[i - ma_period + 1:i + 1])
        sum_vol = np.sum(volumes[i - ma_period + 1:i + 1])
        rsi_vwma[i] = sum_rsi_vol / sum_vol

    return rsi_vwma


async def check_crossing(rsi: np.ndarray, rsi_vwma: np.ndarray) -> Optional[str]:
    if rsi[-2] < rsi_vwma[-2] and rsi[-1] > rsi_vwma[-1]:
        return 'BUY'
    elif rsi[-2] > rsi_vwma[-2] and rsi[-1] < rsi_vwma[-1]:
        return 'SELL'


async def create_message(
        symbol: str,
        interval: str,
        crossing_status: str,
        rsi: np.ndarray) -> str:

    rsi: float = round(float(rsi[-1]), 2)
    status_emoji: str = '\U0001F7E2' if crossing_status == 'BUY' else '\U0001F534'
    symbol: str = f'{symbol}'
    price_symbol: float = float(await get_price_symbol(symbol))
    text_interval: str = await get_interval_text(interval, 'ru')

    return (f'<b>{symbol}</b>\n'
            f'\n'
            f'<b>{status_emoji} {crossing_status}</b>\n'
            f'\U0001F551 {text_interval} [{interval}]\n'
            f'\U0001F4CA RSI {rsi}\n'
            f'\n'
            f'<i>\U0001F4B8 {price_symbol}</i>\n')


async def handle_storage_sent_notifications() -> None:
    while True:
        await asyncio.sleep(1800)
        storage_sent_notifications.clear()
