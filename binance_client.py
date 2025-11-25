from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv
import os

class BinanceClient:
    
    
    def __init__(self, api_key: str = None, api_secret: str = None):
        load_dotenv()
        if api_key is None:
            api_key = os.getenv("API_KEY")
        if api_secret is None:
            api_secret = os.getenv("API_SECRET")

        if not api_key or not api_secret:
            raise SystemExit("API_KEY e API_SECRET não definidos (args ou .env)")

        self.api_key = api_key
        self.api_secret = api_secret
        
        self.client = Client(api_key, api_secret, testnet=True)

    def get_price(self, symbol: str):
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker["price"])
        except Exception as e:
            print("Erro ao buscar preço:", e)

    def market_buy(self, symbol: str, quantity: float):
        try:
            return self.client.order_market_buy(symbol=symbol, quantity=quantity)
        except Exception as e:
            print("Erro compra:", e)

    def market_sell(self, symbol: str, quantity: float):
        try:
            return self.client.order_market_sell(symbol=symbol, quantity=quantity)
        except Exception as e:
            print("Erro venda:", e)
