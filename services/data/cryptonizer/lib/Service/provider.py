import os
import sys
import json
import asyncio
import logging
import ccxt.async_support as ccxt
from collections import defaultdict
from decimal import Decimal
from datetime import datetime

logger = logging.getLogger(__name__)

class Provider:
    def __init__(self, transport):
        self.rc = transport

    async def run_all_exchanges(self, exchange_id):
        results = defaultdict(dict)
        details = defaultdict(dict)
        exchange = getattr(ccxt, exchange_id)({
            'enableRateLimit': True,
            'options': {
                'useWebapiForFetchingFees': False,
            }
        })

        markets = await self.load_markets(exchange)
        for symbol_id in markets.keys():
            logger.info(f'Exchange: {exchange_id}::{symbol_id}')
            data = await self.get_data(exchange, symbol_id)
        await exchange.close()
        return results

    async def get_data(self, exchange, symbol_id):
        ticker = await self.fetch_ticker(exchange, symbol_id)
        orderbook = await self.fetch_orderbook(exchange, symbol_id)
        if self.rc is not None:
            msg_id = await self.rc.xadd(str(exchange).upper()+'::'+symbol_id, {'ticker': json.dumps(ticker), 'orderbook': json.dumps(orderbook)})
        return {'ticker': ticker, 'orderbook': orderbook}

    async def load_markets(self, exchange):
        try:
            result = await exchange.load_markets()
            return result
        except ccxt.BaseError as e:
            logger.error(type(e).__name__, str(e), str(e.args))
            raise e


    async def fetch_ticker(self, exchange, symbol):
        try:
            result = await exchange.fetch_ticker(symbol)
            return result
        except ccxt.BaseError as e:
            logger.warning(type(e).__name__, str(e), str(e.args))
            raise e


    async def fetch_orderbook(self, exchange, symbol):
        try:
            result = await exchange.fetch_order_book(symbol)
            return result
        except ccxt.BaseError as e:
            logger.warning(type(e).__name__, str(e), str(e.args))
            raise e


    async def forever(self, keys):
        while True:
            now = datetime.now()
            logger.info(f"Started at second: {now.second}...")
            if now.second == 0 or now.second == 00:
                for exchange in keys.keys():
                    tasks = [self.run_all_exchanges(exchange) for exchange in keys.keys()]
                    results = asyncio.gather(*tasks)
            else:
                ter = 60 - now.second
                logger.info(f'Will sleep for {ter} seconds zZ')
                await asyncio.sleep(ter)
