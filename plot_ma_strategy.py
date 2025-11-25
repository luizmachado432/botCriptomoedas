import matplotlib.pyplot as plt

def plot_ma_strategy(df):
    #cria a tela em branco
    plt.figure(figsize=(14,6))
    plt.plot(df['close'], label='Preço', linewidth=1.2)
    if 'MA_SHORT' in df.columns:
        plt.plot(df['MA_SHORT'], label='MA Curta', linewidth=1.1)
    if 'MA_LONG' in df.columns:
        plt.plot(df['MA_LONG'], label='MA Longa', linewidth=1.1)

    buy_points = df[df['position'] == 1]
    sell_points = df[df['position'] == -1]

    if not buy_points.empty:
        plt.scatter(buy_points.index, buy_points['close'], marker='^', s=100, color='green', label='BUY')
    if not sell_points.empty:
        plt.scatter(sell_points.index, sell_points['close'], marker='v', s=100, color='red', label='SELL')

    plt.title("Moving Average Crossover")
    plt.xlabel("Indice de candle")
    plt.ylabel("Preço")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
