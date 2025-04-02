import yfinance as yf
from django.core.cache import cache
from datetime import timedelta
import asyncio
from yahooquery import Ticker

from django.core.cache import cache
from yahooquery import Ticker

def obter_cotacao(tickers):
    cache_key = "cotacao_key"
    cotacao = cache.get(cache_key)

    if not cotacao:
        ativos = [f"{ticker}.SA" for ticker in tickers]
        tickers_obj = Ticker(ativos)
        price = tickers_obj.price

        resultados = {}
        for ativo in ativos:
            resultados[ativo] = price.get(ativo, {}).get("regularMarketPrice")

        cache.set(cache_key, resultados, timeout=600)  # Armazena todas as cotações por 5 minutos
        return resultados

    return cotacao

# # Função para formatar preços como moeda
# def formatar_moeda(valor):
#     if isinstance(valor, (int, float)):
#         return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
#     return valor


# # Função para obter cotações em tempo real com cache
# def obter_cotacao1(tiket):    
#     # Tentando pegar a cotação do cache
#     cache_key = f"cotacao_{tiket}"
#     cotacao = cache.get(cache_key)

#     if not cotacao:
#         # Se não encontrar a cotação no cache, faz a requisição
#         ticker = yf.Ticker(f"{tiket}.SA")
#         historico = ticker.history(period="1d", interval="1m")  # Exibe o histórico de cotação do dia
#         preco_final = historico['Close'].iloc[-1]  # Pega a cotação mais recente do dia

#         # Formata a cotação e armazena no cache por 10 minutos
#         cotacao = formatar_moeda(preco_final)
#         cache.set(cache_key, cotacao, timeout=60*30)  # Timeout de 5 minutos
#     return cotacao
