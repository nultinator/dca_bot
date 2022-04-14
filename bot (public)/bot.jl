import Pkg
Pkg.add("PyCall")
Pkg.add("JSON")
using PyCall
using JSON
using Dates

Southx = pyimport("Southxchange")
Southx.Southxchange("Private", "Secret") #Add your API keys here
Market = Southx.Market()
Markets = Southx.Markets()
Wallets = Southx.Wallets()

function getprice()
    Markets.price("yec", "btc")["Ask"]
end

function getbalances()
    JSON.parse(Wallets.balances())
end

function buy()
    price = getprice()
    Market.placeorder("yec", "btc", amount=1, type="BUY", limitprice=price)
    sleep(1)
    println(getbalances())
end

while 1 == 1
    buy()
    sleep(3600)
end