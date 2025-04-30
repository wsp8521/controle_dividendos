
from django.core.cache import cache
from datetime import timedelta
from yahooquery import Ticker

from django.core.cache import cache
from yahooquery import Ticker

def obter_cotacao(tickers):
    # Definir chave única por ativo
    ativos = [f"{ticker}.SA" for ticker in tickers]
    cache_key = f"cotacao_key_{','.join(ativos)}"
    cotacao = cache.get(cache_key)

    if not cotacao:
        tickers_obj = Ticker(ativos)
        price = tickers_obj.price

        resultados = {}
        for ativo in ativos:
            resultados[ativo] = price.get(ativo, {}).get("regularMarketPrice")

        # Cache por mais tempo (ex: 1 hora, se os dados não mudam frequentemente)
        cache.set(cache_key, resultados, timeout=3600)
        return resultados

    return cotacao
