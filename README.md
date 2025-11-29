# botCriptomoedas
Bot de trading automatizado que opera na Binance Testnet usando estratégia de médias móveis. Desenvolvido em Python para fins educacionais.

## Ambiente virtual:
  python -m venv venv
  
  venv\Scripts\activate # Windows

## Dependências:
  pip install -r requirements.txt

## Configure as chaves API:
  Acesse: https://testnet.binance.vision/  
  Gere API Key e Secret Key  
  Na pasta do projeto, crie um arquivo chamado `.env` com:
  
    API_KEY=sua_chave_aqui
    API_SECRET=seu_secret_aqui
(Importante:
  Não compartilhe suas chaves,
  use apenas na Testnet (nunca na Binance real) e
  pode usar as mesmas chaves sempre)

## Como Usar: 
  Execute o bot: python app.py
  
  Configuração inicial:  
    Par de moedas: ETHUSDT, BTCUSDT, etc.  
    Capital inicial: 1000 USDT  
    MA curta: 9 períodos  
    MA longa: 21 períodos  
    Intervalo: 1m, 5m, etc.  
    Atualização: 10 segundos  

## Menu principal:
```
  1 - Iniciar bot
  2 - Status do portfolio  
  3 - Forçar COMPRA
  4 - Forçar VENDA
  5 - Mostrar gráfico
  6 - Sair
```
# Estrutura do Projeto:
```
  app.py                 # Aplicação principal
  binance_client.py      # Conexão com API Binance
  portfolio.py           # Gerenciamento de portfólio
  logger_io.py           # Sistema de logs (CSV/JSON)
  strategies/
  └── ma_crossover.py    # Estratégia trading
  plot_ma_strategy.py    # Gráficos
  data/                  # Dados salvos
```

## Fluxo:
 <pre>
  Busca preços da Binance
  Calcula médias móveis
  Identifica sinais de compra/venda
  Executa operações no portfólio virtual
  Salva logs em CSV/JSON
</pre>

## Saídas
```
  trades.csv:
  timestamp,type,price,quantity
  2024-01-15T10:30:00,BUY,2500.50,0.04
  
  trades.json:
  [{"timestamp": "2024-01-15T10:30:00", "type": "BUY", ...}]
```

## *ESTE PROJETO É APENAS PARA FINS EDUCACIONAIS*

Não use dinheiro real, apenas Binance Testnet
