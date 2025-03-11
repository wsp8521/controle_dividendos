from yahooquery import Ticker

ativos = ["CMIG4.SA", "VALE3.SA", "KDIF11.SA", "MXRF11.SA", "BBSE3.SA", "XPML11.SA", "B3SA3.SA", "KLBN11.SA", "BODB11.SA"]

tickers = Ticker(ativos)
cotacoes = tickers.price

for ativo in ativos:
    print(f'Ativo: {ativo} - Cotação: {cotacoes[ativo]["regularMarketPrice"]}')
