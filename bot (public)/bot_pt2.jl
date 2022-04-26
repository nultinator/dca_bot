import Pkg
Pkg.add("PyCall")
Pkg.add("JSON")
using PyCall
using JSON
using Dates
using Statistics

Southx = pyimport("Southxchange")
Southx.Southxchange("Private", "Secret") #Add your API keys here
Market = Southx.Market()
Markets = Southx.Markets()
Wallets = Southx.Wallets()

function getprice()
    Markets.price("yec", "btc")["Ask"]
end

function getbalances(coin::String)
    coins = JSON.parse(Wallets.balances())
    for Dict in coins
        if Dict["Currency"] == coin
            balance = Dict["Available"]
            return balance
        end
    end
end
function getallhistory()
    Markets.history("yec", "btc", 0, Dates.value(now()))
end
function hilo()
    history = getallhistory()
    highs = []
    lows = []
    for day in history
        date = parse(DateTime, day["Date"])
        if Dates.value(date) > Dates.value(now() - Dates.Day(7))
            high = day["PriceHigh"]
            low = day["PriceLow"]
            push!(highs, high)
            push!(lows, low)
        end
    end
    return Dict("High" => mean(highs), "Low" => mean(lows))
end
function balance_alert()
    run(`./yecshell send your_y_address_goes_here 1 "warning low BTC balance"`)
end

function buy()    
    avg_high = hilo()["High"]
    avg_low = hilo()["Low"]
    price = getprice()
    btc_balance = getbalances("BTC")
    if price > avg_high * 1.1
        message = "Price is more than 10% outside volatilty, NEVER CHASE A CANDLE"
    elseif price * 2 < btc_balance && price < avg_low
        Market.placeorder("yec", "btc", amount=2, type="BUY", limitprice=price)
        message = "Bought 2 YEC, they're on sale!"
    elseif price < btc_balance
        Market.placeorder("yec", "btc", amount=1, type="BUY", limitprice=price)
        message = "Conditions are normal, bought 1 YEC"
    else
        message = "Could not execute order due to low balance"
        balance_alert()
    end
    println(message)

end


while 1 == 1
    buy()
    sleep(3600)
end