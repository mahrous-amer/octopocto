import asyncio
import json
import logging
import logging.config
import time
import configparser
import os
import sys
import redis
import ccxt.async_support as ccxt
import pandas as pd
from collections import defaultdict
from decimal import Decimal

class Provider:

    async def run_all_exchanges(self, keys):
        results = defaultdict(dict)

        for exchange_id in keys.keys():

            exchange = getattr(ccxt, exchange_id)({
                'enableRateLimit': True,
                'options': {
                    'useWebapiForFetchingFees': False,
                }
            })

            print('Exchange:', exchange_id)
            markets = await self.load_markets(exchange)
            for symbol_id in markets.keys():
                ticker = await self.fetch_ticker(exchange, symbol_id)
                results[exchange_id+symbol_id]['Ticker'] = ticker
                #orderbook = await fetch_orderbook(exchange, symbol_id)
                #results[exchange_id+symbol_id]['OrderBook'] = orderbook
                pretty = json.dumps(results[exchange_id+symbol_id]['Ticker'], indent=4, sort_keys=True)
                print(pretty)
            await exchange.close()
        return results


    async def load_markets(self, exchange):
        try:
            result = await exchange.load_markets()
            return result
        except ccxt.BaseError as e:
            print(type(e).__name__, str(e), str(e.args))
            raise e


    async def fetch_ticker(self, exchange, symbol):
        try:
            result = await exchange.fetch_ticker(symbol)
            return result
        except ccxt.BaseError as e:
            print(type(e).__name__, str(e), str(e.args))
            raise e


    async def fetch_orderbook(self, exchange, symbol):
        try:
            result = await exchange.fetch_order_book(symbol)
            return result
        except ccxt.BaseError as e:
            print(type(e).__name__, str(e), str(e.args))
            raise e


    async def forever(self, verbose, keys):
        while True:
            results = await self.run_all_exchanges(keys)
