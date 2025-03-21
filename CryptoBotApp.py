from flask import Flask, render_template, request, jsonify
from CryptoBot import CryptoBot

class CryptoBotApp:
    def __init__(self, api_key, secret_key):
        self.bot = CryptoBot(api_key, secret_key)  # Initialize your CryptoBot instance
        self.app = Flask(__name__)  # Initialize Flask app
        self.setup_routes()  # Set up routes for the web app

    def setup_routes(self):
        @self.app.route('/')
        def index():
            # Render the homepage
            return render_template('index.html')

        @self.app.route('/run-bot', methods=['POST'])
        def run_bot():
            # Run the trading bot
            result = self.bot.run()
            return jsonify({"result": result})

        @self.app.route('/balance')
        def balance():
            # Get account balance
            balance = self.bot.account_balance()
            return jsonify({"balance": balance})

    def run(self):
        self.app.run(debug=True)  # Start the Flask web server

if __name__ == "__main__":
    # Initialize CryptoBotApp with API keys and run the web app
    app = CryptoBotApp(
        api_key="JR5fisLQPPnfgqqAamZXe9F2uGheZjdlVtYoULSwUhGT8Dl7v27URVwL58qbU81z",
        secret_key="fRt0IIH6a0TmeB7HKVvyxqvpyTfec1delTvkZ4hZg95lSiu9MoHpplJgA460jlyK"
    )
    app.run()