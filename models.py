from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        # URL da TESTNET para Spot Trading
        self.TESTNET_URL = "https://testnet.binance.vision"

        # Instancia o client
        self.client = Client(api_key, api_secret)
        self.client.API_URL = self.TESTNET_URL

    # Consulta o preço atual de um símbolo
    def get_price(self, symbol: str):
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker["price"])
        except BinanceAPIException as e:
            print("Erro API:", e)
        except Exception as e:
            print("Erro inesperado:", e)

    # Consulta saldo
    def get_balance(self, asset: str):
        try:
            account = self.client.get_account()
            balances = account["balances"]

            for b in balances:
                if b["asset"] == asset:
                    return float(b["free"])

            return 0.0
        except Exception as e:
            print("Erro ao consultar saldo:", e)

    # Cria uma ordem de mercado
    def market_buy(self, symbol: str, quantity: float):
        try:
            order = self.client.order_market_buy(
                symbol=symbol,
                quantity=quantity
            )
            return order
        except BinanceOrderException as e:
            print("Erro na ordem:", e)
        except BinanceAPIException as e:
            print("Erro API:", e)

    def market_sell(self, symbol: str, quantity: float):
        try:
            order = self.client.order_market_sell(
                symbol=symbol,
                quantity=quantity
            )
            return order
        except BinanceOrderException as e:
            print("Erro na ordem:", e)
        except BinanceAPIException as e:
            print("Erro API:", e)
