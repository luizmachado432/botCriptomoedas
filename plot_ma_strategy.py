import matplotlib.pyplot as plt

#define uma funcao chamada plot_ma_strategy que aceita um unico argumento df
#df e esperado ser um dataframe do pandas contendo os dados do mercado e os sinais da estrategia
def plot_ma_strategy(df):
    #cria uma nova figura a janela ou tela do grafico com um tamanho especifico
    #figsize 14 6 define a largura e a altura da figura
    plt.figure(figsize=(14,6))
    
    #desenha a linha principal do grafico
    #dfclose diz para usar os valores da coluna close do dataframe como o eixo y
    #labelpreco define o texto que aparecera na legenda para esta linha
    plt.plot(df['close'], label='Preço', linewidth=1.2)
    
    #verifica se a coluna ma_short existe no dataframe antes de tentar plota-la
    #isso torna a funcao mais robusta evitando erros caso a coluna nao tenha sido calculada
    if 'MA_SHORT' in df.columns:
        #se a coluna existir desenha a linha da media movel curta
        plt.plot(df['MA_SHORT'], label='MA Curta', linewidth=1.1)
        
    #faz a mesma verificacao para a coluna ma_long
    if 'MA_LONG' in df.columns:
        #se a coluna existir desenha a linha da media movel longa
        plt.plot(df['MA_LONG'], label='MA Longa', linewidth=1.1)

    #cria um novo dataframe chamado buy_points
    #ele contem apenas as linhas do dataframe original df onde o valor da coluna position e igual a 1 sinal de compra
    buy_points = df[df['position'] == 1]
    
    #cria um novo dataframe chamado sell_points
    #ele contem apenas as linhas onde o valor da coluna position e igual a -1 sinal de venda
    sell_points = df[df['position'] == -1]

    #define o titulo que aparecera no topo do grafico
    plt.title("Moving Average Crossover")
    
    #define o rotulo do eixo x horizontal
    plt.xlabel("Indice de candle")
    
    #define o rotulo do eixo y vertical
    plt.ylabel("Preço")
    
    #adiciona a legenda ao grafico usando os labels definidos nos comandos de plot e scatter
    plt.legend()
    
    #adiciona uma grade grid ao fundo do grafico para facilitar a leitura dos valores
    plt.grid(True)
    
    #ajusta automaticamente o espacamento dos elementos do grafico 
    plt.tight_layout()
    
    #exibe a janela com o grafico que foi construido passo a passo
    plt.show()