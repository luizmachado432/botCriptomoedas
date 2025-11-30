import csv 
import os  
import json  
from typing import Dict 

# --- preparaçao dos Arquivos de Log ---

#define o nome e o local do arquivo que guardara o historico das operaçoes
TRADES_CSV = os.path.join("data", "trades.csv")

#cria a pasta "data" se ela ainda nao existir para organizar os arquivos de log
os.makedirs("data", exist_ok=True)

#define os titulos das colunas que serao usados no arquivo CSV
CSV_FIELDS = ["timestamp", "type", "price", "quantity", "cash_after", "base_after"]

# --- funçoes de salvamento ---

"""
esta funçao adiciona UMA UNICA operaçao ao final do arquivo CSV
ela é ideal para registrar as operações uma a uma a medida que acontecem
"""
def append_trade_csv(trade: Dict):
    #verifica se o arquivo CSV ja existe Se não existir é um arquivo novo
    new_file = not os.path.exists(TRADES_CSV)

    #abre o arquivo em modo 'a' (append) que adiciona conteudo no final sem apagar o que ja existe
    with open(TRADES_CSV, "a", newline="") as f:
        #prepara o "escritor" de CSV para trabalhar com dicionarios e as colunas que definimos
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)

        #se o arquivo for novo escreve a linha do cabeçalho primeiro
        if new_file:
            writer.writeheader()
        
        #escreve os dados da operaçao 'trade' como uma nova linha no arquivo
        writer.writerow({
            "timestamp": trade["timestamp"],
            "type": trade["type"],
            "price": trade["price"],
            "quantity": trade["quantity"],
            "cash_after": trade.get("cash_after"),
            "base_after": trade.get("base_after")
        })

"""
esta funçao salva o HISToRICO COMPLETO de operaçoes em um arquivo JSON
diferente do CSV ela apaga o arquivo antigo e salva a lista inteira de novo
"""
def save_trades_json(trades, path="data/trades.json"):
    #abre o arquivo em modo 'w' que SOBRESCREVE o conteúdo do arquivo
    with open(path, "w") as f:
        #converte a lista de operaçoes para o formato JSON e salva no arquivo
        #'indent=2' formata o arquivo para que seja facil de ler por uma pessoa
        json.dump(trades, f, indent=2)

