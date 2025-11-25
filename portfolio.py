import json
from datetime import datetime

class Portfolio:
    def __init__(self, initial_cash=0.0):
        self.cash = float(initial_cash)
        self.base = 0.0
        self.history = []
        self.last_price = 0.0

    def update_last_price(self, price: float):
        if price and price > 0:
            self.last_price = float(price)

    def total_value(self, price=None):
        if price is None:
            price = self.last_price
        return self.cash + self.base * price

    def log(self, type, price, qty):
        record = {
            "timestamp": datetime.now().isoformat(),
            "type": type,
            "price": float(price),
            "quantity": float(qty)
        }
        self.history.append(record)
        return record

    # =============================
    #         COMPRA CORRIGIDA
    # =============================
    def buy(self, price, qty):
        price = float(price)
        qty = float(qty)

        # proteção contra bugs
        if price <= 0 or qty <= 0:
            print("$ Compra ignorada: preço ou quantidade inválidos.")
            return None

        cost = qty * price

        if cost > self.cash + 0.0000001:
            print(f"$ Compra ignorada: saldo insuficiente. cash={self.cash}, cost={cost}")
            return None

        self.cash -= cost
        self.base += qty

        return self.log("BUY", price, qty)


    def sell(self, price, qty):
        price = float(price)
        qty = float(qty)

        if price <= 0 or qty <= 0:
            print("$ Venda ignorada: preço ou quantidade invalidos")
            return None

        if qty > self.base + 0.0000001:
            print(f"$ Venda ignorada: quantidade insuficiente. base={self.base}, qty={qty}")
            return None

        self.base -= qty
        self.cash += qty * price

        return self.log("SELL", price, qty)

    def __str__(self):
        total = self.total_value()
        return (
            f"[PORTFÓLIO] cash={self.cash:.2f} USDT | "
            f"base={self.base:.6f} | "
            f"total≈{total:.2f} USDT"
        )
