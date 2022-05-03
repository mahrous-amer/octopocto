import os
import sys
import time
import configparser
import asyncio
from Service.provider import Provider

Filename="config.cfg"
Keys={}

def getExchangeKeys(filename, exchanges):
    config = configparser.ConfigParser()
    global Filename
    Filename = filename
    config.read(Filename)
    for exchange in exchanges:
        key = luno_key = config.get(exchange.upper(), 'key')
        secret = luno_secret = config.get(exchange.upper(), 'secret')
        Keys[exchange] = {'key': key, 'secret': secret}
        print(Keys[exchange])

def run(verbose, filename, args):
    getExchangeKeys(filename, args)
    provider = Provider()
    asyncio.new_event_loop().run_until_complete(provider.forever(verbose, Keys))
