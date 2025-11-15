from binance_client import BinanceClient

client = BinanceClient()

print(client.get_price("BTCUSDT"))
