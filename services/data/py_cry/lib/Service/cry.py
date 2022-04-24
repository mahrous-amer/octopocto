import asyncio
import json
import logging
import time
import configparser
import os
import sys

import ccxt.async_support as ccxt
import pandas as pd

from collections import defaultdict
from decimal import Decimal

logger = logging.getLogger(__name__)
logging.basicConfig()
logger = logging.getLogger('cry_streams')
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

async def run_all_exchanges(exchange_ids):
    results = {}

    for exchange_id in exchange_ids:

        exchange = getattr(ccxt, exchange_id)({
            'enableRateLimit': True,
            'options': {
                'useWebapiForFetchingFees': False,
            }
        })

        print('Exchange:', exchange_id)
        markets = await load_markets(exchange)
        for symbol_id in markets.keys():
            print('Symbol:', symbol_id)
            ticker = await fetch_ticker(exchange, symbol_id)
            print('Tick:', ticker)
            #orderbook = await fetch_orderbook(exchange, symbol_id)
            #results[exchange_id+symbol_id] = ticker
            #pretty = json.dumps(results[exchange_id+symbol_id], indent=4, sort_keys=True)
        await exchange.close()
    return results


async def load_markets(exchange):
    try:
        result = await exchange.load_markets()
        return result
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e


async def fetch_ticker(exchange, symbol):
    try:
        result = await exchange.fetch_ticker(symbol)
        return result
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e


async def fetch_orderbook(exchange, symbol):
    try:
        result = await exchange.fetch_order_book(symbol)
        return result
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e


async def forever():
    while True:
        exchange_ids = ['luno', 'kraken', 'binance']
        results = await run_all_exchanges(exchange_ids)

if __name__ == '__main__':
   asyncio.new_event_loop().run_until_complete(forever())
