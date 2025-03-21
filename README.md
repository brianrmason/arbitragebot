# CryptoBot Web App

## Overview

CryptoBot is a Python-based cryptocurrency trading bot that utilizes the Binance API to detect 
triangular arbitrage opportunities. This web application provides a simple interface for running 
the bot and checking account balances via a Flask web server. 
NOTE: ****This is on the Binance test network and is not using real money****

## Features

Runs a trading bot that detects triangular arbitrage opportunities.

Fetches and displays the account balance from Binance.

Simple web interface using Flask and HTML/CSS.

Uses Binance API for live trading and market data.

## Prerequisites

To run this project, you need:

Python 3.x

A Binance account

Binance API keys (API Key & Secret Key)

Flask installed in your Python environment

## Installation

Clone the Repository

Install Required Dependencies

Note: Ensure binance and flask libraries are installed.

Set Up API Keys
Replace the API key and secret key in CryptoBotApp.py with your Binance API credentials:

## Usage

Run the Flask Web App

Access the Web Interface
Open a browser and go to:

## Available Features:

Click "Run Bot" to start the trading bot.

Click "Check Balance" to view the Binance account balance.

## Project Structure

### Notes

Testnet Mode: The bot is set to run in Binance testnet mode (testnet=True). To use the live environment, remove this flag.

Risk Disclaimer: This bot executes real trades when connected to a live account. Use it responsibly and at your own risk.

## License

This project is open-source and available under the MIT License.
