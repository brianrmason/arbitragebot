from binance import Client
import time
from itertools import combinations


"""
The class Cryptobot interfaces with the Binance API to check the cryptocurrency 
market for arbitrage opportunities. When we create an instance of the CryptoBot 
class, we call the Client class from the Binance API to laod the API key and 
secret key. Also, the fee, profit threshold, and number of iterations is initialized. 
"""
class CryptoBot:
    def __init__(self, api_key, secret_key, fee=0.0015, profit_threshold=1.0, iterations=100):
        self.client = Client(api_key, secret_key, tld='us', testnet=True)
        self.fee = fee
        self.profit_threshold = profit_threshold
        self.iterations = iterations


    def run(self):
        """
        The run fuction will be called to run all of the other functions within the CryptoBot class. 
        """
        n = 0
        while n < self.iterations:
            if n > 0:
                time.sleep(3)
            n += 1

            symbols = self.get_all_symbols()
            triangles = self.find_triangular_pairs(symbols)

            for triangle in triangles:
                profit = self.calculate_profit(triangle)
                trade_executed = self.execute_trade(profit, triangle)

                if trade_executed:
                    print(f"Trade was made for triangle: {triangle}")
                else:
                    print(f"No trade was made for triangle: {triangle}")

            total_balance = self.account_balance()
            print(f"\nCurrent Account Balance: {total_balance:,} USD\n")

    def get_all_symbols(self):
        """
        This function pulls all of the symbol names from Binance
        """
        exchange_info = self.client.get_exchange_info()
        symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['status'] == 'TRADING']
        return symbols

    def find_triangular_pairs(self, symbols):
        """ 
        This function takes in the parameter symbols and makes combinations of three 
        out of the symbols and adds them to the valide_triangles array
        """
        pairs = combinations(symbols, 3)
        valid_triangles = []

        for pair in pairs:
            if self.is_valid_triangle(pair):
                valid_triangles.append(pair)

        return valid_triangles


    def is_valid_triangle(self, pair):
        """
        The first condition ensures that the first and second pair share the same base, 
        the second and third pair share the same quote, and the third and first pair share 
        the same base and quote. The second condition ensures that the first pair's base 
        matches the second pair's quote, the first pair's quote matches the third pair's base, 
        and the third pair's quote matches the second pair's base.
        """
        base1, quote1 = pair[0][:3], pair[0][3:]
        base2, quote2 = pair[1][:3], pair[1][3:]
        base3, quote3 = pair[2][:3], pair[2][3:]

        return (
            (base1 == base2 and quote1 == quote3 and base3 == quote2) or
            (base1 == quote2 and quote1 == base3 and quote3 == base2)
        )

    def calculate_profit(self, triangle):
        """
        This function tells whether a trianglular trade is profitable or not. The function calculates the bid and ask profit 
        and calculates fees (self.fee) to detect if the trade is worth making. 
        """
        first_pair = self.check_pair(triangle[0])
        second_pair = self.check_pair(triangle[1])
        third_pair = self.check_pair(triangle[2])

        bid_profit = (float(first_pair[0]) * (1 - self.fee) * float(second_pair[0]) * (1 - self.fee) * float(third_pair[0]) * (1 - self.fee)) / (
            float(first_pair[1]) * (1 + self.fee) * float(second_pair[1]) * (1 + self.fee) * float(third_pair[1]) * (1 + self.fee)) - 1

        ask_profit = (float(first_pair[1]) * (1 + self.fee) * float(second_pair[1]) * (1 + self.fee) * float(third_pair[1]) * (1 + self.fee)) / (
            float(first_pair[0]) * (1 - self.fee) * float(second_pair[0]) * (1 - self.fee) * float(third_pair[0]) * (1 - self.fee)) - 1 

        return bid_profit, ask_profit

    def execute_trade(self, profit, triangle):
        """
        This function exectues the trade based off if the profit is greater than the profit 
        threshold, which can be adjusted based off of the user's preference. 
        """
        if profit[0] * 100 > self.profit_threshold: 
            amount_1 = 1
            amount_2 = float(amount_1) * (1 - self.fee) * float(self.check_pair(triangle[0])[0]) / (1 + self.fee) / float(self.check_pair(triangle[1])[1])
            amount_3 = float(amount_2) * (1 - self.fee) * float(self.check_pair(triangle[1])[0]) / (1 + self.fee) / float(self.check_pair(triangle[2])[1])

            self.client.order_market_sell(symbol=triangle[0], quantity=amount_1)
            self.client.order_market_buy(symbol=triangle[1], quantity=amount_2)
            self.client.order_market_sell(symbol=triangle[2], quantity=amount_3)
            return True
        
        elif profit[1] * 100 > self.profit_threshold: 
            amount_3 = 1
            amount_2 = float(amount_3) * (1 - self.fee) * float(self.check_pair(triangle[2])[1]) / (1 + self.fee) * float(self.check_pair(triangle[1])[0])
            amount_1 = float(amount_2) * (1 - self.fee) * float(self.check_pair(triangle[1])[1]) / (1 + self.fee) * float(self.check_pair(triangle[0])[0])

            self.client.order_market_sell(symbol=triangle[2], quantity=amount_3)
            self.client.order_market_sell(symbol=triangle[1], quantity=amount_2)
            self.client.order_market_buy(symbol=triangle[0], quantity=amount_1)
            return True

        else: 
            return False

    def check_pair(self, symbol):
        """
        Helper function to check pairs of coins needed in the calculate_profit function
        """
        depth = self.client.get_orderbook_tickers(symbol=symbol)
        return depth["bidPrice"], depth["askPrice"]

    def account_balance(self):
        """
        Simple account balance check function 
        """
        btc_balance = self.client.get_asset_balance(asset='BTC')['free']
        ltc_balance = self.client.get_asset_balance(asset='LTC')['free']
        usdt_balance = self.client.get_asset_balance(asset='USDT')['free']

        btc_price = self.client.get_avg_price(symbol='BTCUSDT')['price']
        ltc_price = self.client.get_avg_price(symbol='LTCUSDT')['price']

        usdt_total = float(usdt_balance)
        btc_total = float(btc_balance) * float(btc_price)
        ltc_total = float(ltc_balance) * float(ltc_price)

        total_balance = float(btc_total) + float(ltc_total) + usdt_total

        return round(total_balance, 2)