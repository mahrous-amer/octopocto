import os
import sys
import json
import time
import logging
import ccxt
from collections import defaultdict
from decimal import Decimal
from datetime import datetime

logger = logging.getLogger(__name__)

class Actuator:
    def __init__(self, transport):
        self.rc = transport

    def get_data(self, exchange_id):
        markets = self.load_markets(exchange_id)
        for symbol_id in markets.keys():
            stream = str(exchange_id).upper()+'::'+symbol_id
            logger.info(f'Exchange: {stream}')
            try:
                data = self.rc.xreadgroup(str(stream))
                logger.info(data)
                if data != None and data != []:
                    [[stream, [[number, d]]]] = data
                    self.rc.ack(str(stream), str(number))
                self.rc.remove_group(str(stream))
            except Exception as e:
                raise e


    def load_markets(self, exchange_id):
        try:
            exchange = getattr(ccxt, exchange_id)({
                'enableRateLimit': True,
                'options': {
                    'useWebapiForFetchingFees': False,
                }
            })
            result = exchange.load_markets()
            return result
        except ccxt.BaseError as e:
            logger.error(type(e).__name__, str(e), str(e.args))
            raise e

    def forever(self, keys):
        while True:
            now = datetime.now()
            logger.info(f"Started at second: {now.second}...")
            if now.second == 00:
                for exchange in keys.keys():
                    self.get_data(exchange)
            else:
                ter = 60 - now.second
                logger.info(f'Will sleep for {ter} seconds zZ')
                time.sleep(ter)
