from binance_client import BinanceClient

client = BinanceClient()

valor = client.get_price("BTCUSDT")

print(f"Preço atual do BTC USDT: {valor}")
