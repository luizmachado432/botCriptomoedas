import numpy as np
import pandas as pd
from .strategy_base import TradingStrategy

class MovingAverageCrossover(TradingStrategy):
    def __init__(self, short_period: int = 10, long_period: int = 30):
        if short_period >= long_period:
            raise ValueError("O período curto deve ser menor que o período longo")

        self.short = int(short_period)
        self.long = int(long_period)

    def compute_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        
        df = df.copy()
        # calcula a media movel curta (MA_SHORT)
        #.rolling(self.short) cria uma "janela" movel com os últimos 'self.short' preços
        #.mean() calcula a média dos preços dentro dessa janela
        df['MA_SHORT'] = df['close'].rolling(self.short).mean()
        
        #calcula a media movel longa (MA_LONG)
        #o mesmo processo, mas usando o período longo para capturar a tendência principal
        df['MA_LONG'] = df['close'].rolling(self.long).mean()
        
        #cria o "sinal" direcional da tendência
        #a função np.where é uma formade fazer uma condição "se/senao"
        #se a Media Curta está ACIMA da media longa, o sinal é 1 (sugere tendência de alta)
        #caso contrario, o sinal é -1 (sugere tendência de baixa)
        df['signal'] = np.where(df['MA_SHORT'] > df['MA_LONG'], 1, -1)
        
        # identifica o "gatilho" do cruzamento (o momento exato da mudança de sinal)
        #.diff() calcula a diferença entre o 'signal' da linha atual e o da linha anterior
        #quando ocorre um cruzamento de COMPRA o sinal muda de -1 para 1. A diferença é: 1 - (-1) = 2
        #quando ocorre um cruzamento de VENDA o sinal muda de 1 para -1. A diferença é: -1 - 1 = -2
        #um valor 0 significa que não houve cruzamento (a tendência se manteve)
        #.fillna(0) preenche o primeiro valor (que será NA/vazio pois nao tem linha anterior) com 0
        df['position'] = df['signal'].diff().fillna(0)

        return df
