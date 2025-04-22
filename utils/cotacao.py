
from django.core.cache import cache
from datetime import timedelta
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

