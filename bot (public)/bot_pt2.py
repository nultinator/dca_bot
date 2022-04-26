#!/bin/python3
import Southxchange
import json
import time
import datetime

Southxchange.Southxchange('Private', 'Secret') #Use your API keys here
Market = Southxchange.Market()
Markets = Southxchange.Markets()
Wallets = Southxchange.Wallets()
time.sleep(1)

#print(Markets.price('yec', 'btc'))

def getbalances(coin):
    currencies = json.loads(Wallets.balances())
    for dict in currencies:
        if dict['Currency'] == coin:
            balance = dict['Available']
            return(balance)

def hilo():
    unixtime = int(datetime.datetime.timestamp(datetime.datetime.now())) * 1000
    start_time = unixtime - 604800000 #Current time - one week in milliseconds
    end_time = unixtime
    history = Markets.history('yec', 'btc', start_time, end_time, periods=7)
    highs = []
    lows = []
    for dict in history:
        high = dict['PriceHigh']
        low = dict['PriceLow']
        highs.append(high)
        lows.append(low)
    hi = sum(highs) / 8 #We're dividing by 8 because we get 7 days of history plus today
    lo = sum(lows) / 8
    return {'high': hi, 'low': lo}

print(getbalances('BTC'))
time.sleep(1)
print(getbalances('YEC'))
time.sleep(1)

def buy():
    avg_high = hilo()['high']
    avg_low = hilo()['low']
    btc_balance = getbalances('BTC')
    price = Markets.price('yec', 'btc')['Ask']
    if price > avg_high * 1.1: #Don't buy if price is more than 10% higher than the avg_high
        print("Price is up more than 10%, NEVER CHASE A CANDLE")
    elif price * 2 < btc_balance and price < avg_low: #They're cheap, buy extra
        Market.placeorder('YEC', 'BTC', amount=2, type='BUY', limitprice=price)
        print("Bought 2, they're on sale!")
    elif price < btc_balance: #Standard buy
        Market.placeorder('YEC', 'BTC', amount=1, type='BUY', limitprice=price)
        print("Conditions are normal, bought 1 YEC")
    else: #Don't buy because we can't afford it
        print("Could not execute order due to low balance")

a = 1
while a == 1:
    buy()
    time.sleep(3600)