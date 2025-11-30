#este codigo cria um modelo base chamado tradingstrategy
#ele serve como uma regra para todas as outras estrategias
#ele obriga que qualquer estrategia tenha a funcao computesignals
#que e responsavel por calcular os sinais de compra e venda
from abc import ABC, abstractmethod
import pandas as pd

class TradingStrategy(ABC):
    """
    Interface/ABSTRACT base para estratégias.
    """

    @abstractmethod
    def compute_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Recebe DataFrame com ao menos coluna 'close' e retorna df com colunas
        necessárias (ex: MA_SHORT, MA_LONG, signal, position).
        """
        pass