import time
import pandas as pd
from dotenv import load_dotenv
import os

from binance_client import BinanceClient
from portfolio import Portfolio
from strategies.ma_crossover import MovingAverageCrossover
from logger_io import append_trade_csv, save_trades_json
from plot_ma_strategy import plot_ma_strategy

load_dotenv()

def get_historical(client, symbol, interval="1m", limit=200):
    """
    Baixa candles (klines) da Binance via client.client.get_klines
    e retorna DataFrame com coluna 'close' (float).
    """
    candles = client.client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(candles, columns=[
        'time_open','open','high','low','close','volume',
        'time_close','quote_volume','trades',
        'taker_buy_base','taker_buy_quote','ignore'
    ])
    df['close'] = df['close'].astype(float)
    return df

class App:
    def __init__(self):
        self.client = None
        self.portfolio = None
        self.strategy = None
        self.symbol = None
        self.interval = "1m"
        self.poll_seconds = 10

    def configure(self):
        print("Parametros do bot")
        api_key = os.getenv("API_KEY")
        api_secret = os.getenv("API_SECRET")

        # inicializa o client 
        self.client = BinanceClient(api_key, api_secret)

        # parâmetros do usuário
        self.symbol = input("Par de moedas (ex: ETHUSDT, BTCUSDT, BNBUSDT): ").upper().strip() or "ETHUSDT"
        capital = float(input("Capital inicial (USDT) [ex: 1000]: ") or 1000)
        short = int(input("Período MA curta [ex: 9]: ") or 9)
        long = int(input("Período MA longa [ex: 21]: ") or 21)
        self.interval = input("Intervalo de candles (ex: 1m, 5m) [1m]: ") or "1m"
        self.poll_seconds = int(input("Intervalo de atualização (segundos) [10]: ") or 10)

        # cria portfólio e estratégia (note initial_cash)
        self.portfolio = Portfolio(initial_cash=capital)
        self.strategy = MovingAverageCrossover(short, long)

    
    # COMPRA FORÇADA (registra CSV/JSON)
    
    def force_buy(self):
        print(">>> Forçando COMPRA")
        price = self.client.get_price(self.symbol)
        if price is None or price == 0:
            print("$$ Preço não disponível")
            return
        qty = self.portfolio.cash / price
        if qty <= 0:
            print("$$ Sem saldo para comprar")
            return

        # Executa compra no portfólio (paper trading)
        self.portfolio.buy(price, qty)

        # pega o trade registrado pelo Portfolio (último)
        trade = self.portfolio.history[-1]

        # registra no CSV/JSON via logger_io
        append_trade_csv(trade)
        save_trades_json(self.portfolio.history)

        print(f"$$ COMPRA FORÇADA: qty={qty:.6f} a price={price:.2f}")

   
    # VENDA FORÇADA (registra CSV/JSON)
    
    def force_sell(self):
        print(">>> Forçando VENDA")
        price = self.client.get_price(self.symbol)
        if price is None or price == 0:
            print("$$ Preço não disponível")
            return
        qty = self.portfolio.base
        if qty <= 0:
            print("$$ Sem ativo para vender")
            return

        # Executa venda no portfólio (paper trading)
        self.portfolio.sell(price, qty)

        # pega o trade registrado pelo Portfolio (último)
        trade = self.portfolio.history[-1]

        # registra no CSV/JSON via logger_io
        append_trade_csv(trade)
        save_trades_json(self.portfolio.history)

        print(f"$$ VENDA FORÇADA: qty={qty:.6f} a price={price:.2f}")

    # Menu e loop principal
    def run(self):
        self.configure()

        while True:
            print("\n--------- MENU --------")
            print("1 - Iniciar bot")
            print("2 - Status do portfolio")
            print("3 - Forçar COMPRA")
            print("4 - Forçar VENDA")
            print("5 - Mostrar gráfico")
            print("6 - Sair")
            choice = input("> ").strip()

            if choice == "1":
                self.start_bot()
            elif choice == "2":
                try:
                    current_price = self.client.get_price(self.symbol)
                    if current_price:
                        self.portfolio.update_last_price(current_price)
                except Exception:
                    pass
                print(self.portfolio)
            elif choice == "3":
                self.force_buy()
            elif choice == "4":
                self.force_sell()
            elif choice == "5":
                df = get_historical(self.client, self.symbol, interval=self.interval, limit=200)
                df = self.strategy.compute_signals(df)
                plot_ma_strategy(df)
            elif choice == "6":
                print("Saindo")
                break
            else:
                print("Opçao invalida")

    def start_bot(self):
        print("Iniciando BOT")
        poll_seconds = self.poll_seconds

        try:
            while True:
                df = get_historical(self.client, self.symbol, interval=self.interval, limit=200)
                df = self.strategy.compute_signals(df)

                if df.empty or len(df) < max(self.strategy.short, self.strategy.long) + 2:
                    # ainda não há candles suficientes
                    print("$$ Sem dados de candle suficientes")
                    time.sleep(poll_seconds)
                    continue

                # USAR CANDLE FECHADO (penúltimo) para evitar sinais em candle em formação
                last = df.iloc[-2]   # candle fechado
                price = float(last["close"])
                pos = last["position"]

                # DEBUG: mostrar médias e sinal
                ma_short = last.get("MA_SHORT", None)
                ma_long = last.get("MA_LONG", None)
                print("--------------------------------------------------")
                print(f"Preço fechado: {price:.6f}")
                if ma_short is not None and ma_long is not None:
                    print(f"MA_SHORT={ma_short:.6f} | MA_LONG={ma_long:.6f} | position={pos}")
                else:
                    print(f"position={pos}")

                #  COMPRA: MA curta cruzou para cima da MA longa 
                if pos > 0:
                    if self.portfolio.cash > 0:
                        qty = self.portfolio.cash / price
                        if qty > 0:
                            self.portfolio.buy(price, qty)
                            trade = self.portfolio.history[-1]
                            append_trade_csv(trade)
                            save_trades_json(self.portfolio.history)
                            print(f"$$ COMPRA AUTOMÁTICA executada: qty={qty:.6f} price={price:.2f}")
                    else:
                        print("$ Sinal de COMPRA, mas sem saldo")

                #  VENDA: MA curta cruzou para baixo da MA longa 
                elif pos < 0:
                    if self.portfolio.base > 0:
                        qty = self.portfolio.base
                        self.portfolio.sell(price, qty)
                        trade = self.portfolio.history[-1]
                        append_trade_csv(trade)
                        save_trades_json(self.portfolio.history)
                        print(f"$$ VENDA AUTOMÁTICA executada: qty={qty:.6f} price={price:.2f}")
                    else:
                        print("$ Sinal de VENDA, mas sem ativos para vender")

                # Status do portfólio
                total = self.portfolio.total_value(price)
                print(f"[STATUS] dineiro ={self.portfolio.cash:.2f} USDT | ativos={self.portfolio.base:.6f} | total≈{total:.2f} USDT")

                time.sleep(poll_seconds)

        except KeyboardInterrupt:
            print("\nBot encerrado")
        except Exception as e:
            print(" Erro inesperado no loop:", e)
        finally:
            # garante salvar histórico final
            try:
                save_trades_json(self.portfolio.history)
                print("Logs salvos")
            except Exception:
                pass

if __name__ == "__main__":
    App().run()
