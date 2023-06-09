## Brian Mason - 12/23/2022
## import Client class from binance module
from binance import Client
## import python's time module to delay while loop
import time
## import datetime to get date and time for output file
from datetime import datetime


## define variable with API key from Binance
binance_api = "JR5fisLQPPnfgqqAamZXe9F2uGheZjdlVtYoULSwUhGT8Dl7v27URVwL58qbU81z"
## define variable with secret API key from Binance
binance_secret = "fRt0IIH6a0TmeB7HKVvyxqvpyTfec1delTvkZ4hZg95lSiu9MoHpplJgA460jlyK"

## initialize client variable on US testnet
client = Client(binance_api, binance_secret, tld='us', testnet=True)

fee = 0.0015 ## binance fee for VIP1 level trades in US
iterations = 10 ## number of iterations to be carried out


def main():
    n = 0
    now = datetime.now()
    now = str(now)
    while n < iterations:
        if n > 0:
            time.sleep(5)
        n += 1
        ## define varirables to call functions that check prices of trading pairs
        first_pair = check_first_pair()
        second_pair = check_second_pair()
        third_pair = check_third_pair()
        ## define variable to call function to compare ratios of paired coins
        difference = compare_ratios(first_pair, second_pair, third_pair)
        print(f"\nCurrent Triangular Price Difference is ${difference}")
        if float(difference) > 1.25:
            profit = calculate_profit(difference)
            print(f"The Profit For This Trade is an Estimated {difference} USD\n")
            print("Executing Triangular Trade:")
            print("Buying LTC with BTC in LTC/BTC Market")
            print("Selling LTC for USDT in LTC/USDT Market")
            print("Selling USDT for BTC in BTC/USDT Market\n")
            execute = execute_trade(first_pair, second_pair, third_pair)
            # set variables equal to balance of coins used in triangular path
            balance_btc = client.get_asset_balance(asset='BTC')
            balance_ltc = client.get_asset_balance(asset='LTC')
            balance_usdt = client.get_asset_balance(asset='USDT')
            total_balance = account_balance()
            print(f"\nResulting BTC Balance: {balance_btc['free']}\n")
            print(f"\nResulting LTC Balance: {balance_ltc['free']}\n")
            print(f"\nResulting USDT Balance: {balance_usdt['free']}\n")
            print(f"\nCurrent Account Balance: {total_balance:,} USD\n")
            with open("results.csv", "a") as file:
                l1 = "\niCurrent time is: \n"
                l2 = str(now)
                l3 = "\nEstimated Profit: \n"
                l4 = str(difference)
                l5 = "\nNew Account Balance: \n"
                l6 = str(total_balance) + "\n"
                file.writelines([l1, l2, l3, l4, l5, l6])
            print(f"Number of iterations remaining: {iterations - n}\n\n")
            if n == iterations:
                print("\nNumber of Iterations Reached... Exiting Program\n")
            continue
        else:
            print("\nThis Trade is Currently Not Profitable... Carrying Out Remaining Iterations\n")
            print(f"Number of iterations remaining: {iterations - n}")
            if n == iterations:
                print("\nNumber of Iterations Reached... Exiting Program\n")

    # total_balance = account_balance()
    # print(f"\nCurrent Account Balance: {total_balance:,} USD\n")


    # btc_balance = client.get_asset_balance(asset='USDT')
    # free_btc = btc_balance['free']
    # print(free_btc)

    # second = client.order_market_buy(
    # symbol='LTCUSDT',
    # quantity=20)

    # btc_balance = client.get_asset_balance(asset='LTC')
    # free_btc = btc_balance['free']
    # print(free_btc)


def check_first_pair():
    ## Get Price of LTC/BTC from list of prices
    prices = client.get_avg_price(symbol='BTCUSDT')
    return prices["price"]

def check_second_pair():
    # ## Get Price of LCT/USDT from list of prices
    prices = client.get_avg_price(symbol='LTCBTC')
    return prices["price"]

def check_third_pair():
    ## Get Price of BTC/USDT from list of prices
    prices = client.get_avg_price(symbol='LTCUSDT')
    return prices["price"]


def compare_ratios(first_pair, second_pair, third_pair):
    # get account balance of Bitcoin
    usdt_balance = client.get_asset_balance(asset='USDT')
    free_usdt = usdt_balance['free']
    usdt = 0.05 * float(free_usdt)
    x = float(usdt / float(first_pair)) # number of BTC to buy with USDT
    y = float(x / float(second_pair) * float(1 - fee))   # number of LTC to buy with BTC
    z = float(y * float(third_pair))    # amnt USDT to buy with LTC
    difference = float(usdt - z)
    difference = round(difference, 2)
    return float(difference)


def calculate_profit(difference):
    usdt_balance = client.get_asset_balance(asset='USDT')
    free_usdt = usdt_balance['free']
    usdt = 0.05 * float(free_usdt)
    result = float(usdt) - float(difference)
    profit = round(result, 2)
    return profit


def execute_trade(first_pair, second_pair, third_pair):
    usdt_balance = client.get_asset_balance(asset='USDT')
    free_usdt = usdt_balance['free']
    usdt = 0.05 * float(free_usdt)
    x = float(usdt / float(first_pair))
    y = float(x / float(second_pair))
    z = float(y * float(third_pair))

    x = round(x, 2)
    y = round(y, 2)

    # place order using the order_market_buy method
    first = client.order_market_buy(
    symbol='BTCUSDT',
    quantity=x)

    second = client.order_market_buy(
    symbol='LTCBTC',
    quantity=y)

    third = client.order_market_sell(
    symbol='LTCUSDT',
    quantity=y)

    return(first, second, third)


def account_balance():
    btc_balance = client.get_asset_balance(asset='BTC')
    free_btc = btc_balance['free']
    ltc_balance = client.get_asset_balance(asset='LTC')
    free_ltc = ltc_balance['free']
    usdt_balance = client.get_asset_balance(asset='USDT')
    free_usdt = usdt_balance['free']

    btc_price = client.get_avg_price(symbol='LTCBTC')
    avg_btc = btc_price['price']
    ltc_price = client.get_avg_price(symbol='LTCUSDT')
    avg_ltc = ltc_price['price']
    usdt_price = client.get_avg_price(symbol='BTCUSDT')
    avg_usdt = usdt_price['price']

    btc_total = float(free_btc) * float(avg_btc)
    ltc_total = float(free_ltc) * float(avg_ltc)
    usdt_total = float(free_usdt)

    account_balance = float(btc_total) + float(ltc_total) + float(usdt_total)

    return round(account_balance, 2)


if __name__ == "__main__":
    main()




    # btc_balance = client.get_asset_balance(asset='BTC')
    # free_btc = btc_balance['free']
    # print(free_btc)

    # first = client.order_market_buy(
    # symbol='BTCBUSD',
    # quantity=1000)

    # prices = client.get_all_tickers()
    # print(prices)
    # price = client.get_symbol_info('BTCUSDT')
    # print(price)
    # usdt_balance = client.get_asset_balance(asset='USDT')
    # free_usdt = usdt_balance['free']
    # print(free_usdt)


    # btc_balance = client.get_asset_balance(asset='BTC')
    # free_btc = btc_balance['free']
    # ltc_balance = client.get_asset_balance(asset='LTC')
    # free_ltc = ltc_balance['free']
    # usdt_balance = client.get_asset_balance(asset='USDT')
    # free_usdt = usdt_balance['free']

    # print(free_btc, free_ltc, free_usdt)

    # btc_price = client.get_avg_price(symbol='LTCBTC')
    # avg_btc = btc_price['price']
    # ltc_price = client.get_avg_price(symbol='LTCUSDT')
    # avg_ltc = ltc_price['price']
    # usdt_price = client.get_avg_price(symbol='BTCUSDT')
    # avg_usdt = usdt_price['price']

    # btc_total = float(free_btc) * float(avg_btc)
    # ltc_total = float(free_ltc) * float(avg_ltc)
    # usdt_total = float(free_usdt)

    # account_balance = float(btc_total) + float(ltc_total) + float(usdt_total)

    # print(account_balance)