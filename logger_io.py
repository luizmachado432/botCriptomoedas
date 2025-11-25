import csv
import os
import json
from typing import Dict

TRADES_CSV = os.path.join("data", "trades.csv")
os.makedirs("data", exist_ok=True)

CSV_FIELDS = ["timestamp", "type", "price", "quantity", "cash_after", "base_after"]

def append_trade_csv(trade: Dict):
    new_file = not os.path.exists(TRADES_CSV)
    with open(TRADES_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow({
            "timestamp": trade["timestamp"],
            "type": trade["type"],
            "price": trade["price"],
            "quantity": trade["quantity"],
            "cash_after": trade.get("cash_after"),
            "base_after": trade.get("base_after")
        })

def save_trades_json(trades, path="data/trades.json"):
    with open(path, "w") as f:
        json.dump(trades, f, indent=2)
