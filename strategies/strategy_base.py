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
