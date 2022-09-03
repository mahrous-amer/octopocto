import os
import sys
import time
import signal
import yaml
import asyncio
import logging
import logging.config
import configparser
import argparse

import importlib
sys.path.insert(0, '/opt/app/lib/')
from Transport.Redis import Redis
# from Message.Redis import msg
from Service.provider import Provider

logger = logging.getLogger(__name__)
Filename="config.cfg"
Keys={}

def init_argparse() -> None:
    with open('log_config.yml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cfg)
    parser = argparse.ArgumentParser(description=__name__)
    parser.add_argument('-d', '--debug', action='store_true', help='set the logging level to logging.DEBUG')
    args = parser.parse_args()
    if args.debug:
        global logger
        with open('log_config.yml', 'r') as f:
            log_cfg = yaml.safe_load(f.read())
            log_cfg['root']['level'] = 'DEBUG'
        logging.config.dictConfig(log_cfg)
        logger = logging.getLogger(__name__)
        logger.debug('DEBUG MODE ENABLED')

def getExchangeKeys(exchanges, filename=Filename):
    config = configparser.ConfigParser()
    config.read(filename)
    for exchange in exchanges:
        key = config.get(exchange.upper(), 'key')
        secret = config.get(exchange.upper(), 'secret')
        Keys[exchange] = {'key': key, 'secret': secret}

async def run(loop):
    getExchangeKeys(['luno', 'binance', 'kraken'])
    try:
        transport = Redis('cryptonizer')
        await transport.start()
        provider = Provider(transport)
        await provider.forever(Keys)
        await transport.close()
    except Exception as e:
        logger.warning(e)


if __name__ == '__main__':
    init_argparse()
    logger.info('Starting...')
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run(loop))
