import os
import sys
import time
import configparser
import asyncio
from Service.provider import Provider

FILENAME="config.cfg"
Keys={}

def getExchangeKeys(exchanges):
    print(exchanges)
    config = configparser.ConfigParser()
    config.read(FILENAME)
    for exchange in exchanges:
        key = luno_key = config.get(exchange.upper(), 'key')
        secret = luno_secret = config.get(exchange.upper(), 'secret')
        Keys[exchange] = {'key': key, 'secret': secret}
        print(Keys[exchange])

def run(args):
    getExchangeKeys(args)
    provider = Provider()
    asyncio.new_event_loop().run_until_complete(provider.forever(Keys))
