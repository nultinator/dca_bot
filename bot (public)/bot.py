#!/bin/python3
import Southxchange
import json
import time

Southxchange.Southxchange('Private', 'Secret') #Use your API keys here
Market = Southxchange.Market()
Markets = Southxchange.Markets()
Wallets = Southxchange.Wallets()
time.sleep(1)

print(Markets.price('yec', 'btc'))

def getbalances():
    print(json.loads(Wallets.balances()))


getbalances()
time.sleep(1)

def buy():
    price = Markets.price('yec', 'btc')['Ask']
    Market.placeorder('YEC', 'BTC', amount=1, type='BUY', limitprice=price)
    time.sleep(1)
    getbalances()

a = 1
while a == 1:
    buy()
    time.sleep(3600)