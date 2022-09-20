import os
import sys
import json
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
        logger.info(f'Exchange: {exchange_id}')
        markets = self.load_markets(exchange_id)
        for symbol_id in markets.keys():
            logger.info(symbol_id)
            try:
                #data = self.rc.group_info(str(exchange_id).upper()+'::'+symbol_id)
                data = self.rc.xreadgroup(str(exchange_id).upper()+'::'+symbol_id)
                #data = self.rc.remove_group(str(exchange_id).upper()+'::'+symbol_id)
                if data != None and data != []:
                    [[stream, [[number, d]]]] = data
                    self.rc.ack(str(stream), str(number))
            except Exception as e:
                logger.warn(e)


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
            try:
                now = datetime.now()
                for exchange in keys.keys():
                    self.get_data(exchange)
                later = datetime.now()
                if (later - now).total_seconds() < 60:
                    ter = 60 - (later - now).total_seconds()
                    logger.info(f'Will sleep for {ter} seconds zZ')
                    sleep(ter)
            except Exception as e:
                raise e
