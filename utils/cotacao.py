import os
import requests
import time
import logging
from django.core.cache import cache
from dotenv import load_dotenv
load_dotenv()
import hashlib

logger = logging.getLogger(__name__)

def obter_cotacao(ativos):
    """
    Consulta cotações em tempo real para cada ativo individualmente (plano gratuito da Brapi).
    Usa cache individual por ativo com validade de 30 minutos.
    """
    cotacoes = {}
    
    hash = hashlib.md5()
    user_id = hash.hexdigest()  # Simulando um ID de usuário único para o cache

    for ativo in ativos:
        cache_key = f"cotacao_{user_id}_{ativo}"
        preco_cache = cache.get(cache_key)

        if preco_cache is not None:
            cotacoes[ativo] = preco_cache
            continue

        try:
            url = f"https://brapi.dev/api/quote/{ativo}"
            params = {
                'range': '1d',
                'interval': '1d',
                'token': os.getenv('BRAPI_TOKEN'),
            }
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            resultado = data.get("results", [])[0]
            preco = resultado.get("regularMarketPrice")

            if preco is not None:
                cache.set(cache_key, preco, timeout=1800)  # cache 30 minutos
                cotacoes[ativo] = preco
            else:
                logger.warning(f"[Brapi] Preço não disponível para {ativo}")
                cotacoes[ativo] = None

        except Exception as e:
            logger.warning(f"[Brapi] Falha ao buscar {ativo}: {e}")
            cotacoes[ativo] = preco_cache  # usa valor anterior se existir

        time.sleep(0.5)  # respeita limites do plano gratuito

    return cotacoes


# from django.core.cache import cache
# from datetime import timedelta
# from yahooquery import Ticker
# from hashlib import md5

# def obter_cotacao(tickers, user_id):
#     ativos = [f"{ticker}.SA" for ticker in tickers]

#     # Cria uma chave única por usuário e por conjunto de ativos
#     chave_base = f"{user_id}_" + ','.join(sorted(ativos))
#     cache_key = "cotacao_key_" + md5(chave_base.encode()).hexdigest()

#     cotacao = cache.get(cache_key)
#     if cotacao:
#         return cotacao

#     # Aqui usa yfinance ou o método que preferir para buscar os dados reais
#     resultados = {}
#     for ativo in ativos:
#         ticker_obj = Ticker(ativo)
#         resultados[ativo] = ticker_obj.price[ativo].get("regularMarketPrice", None)


#     cache.set(cache_key, resultados, timeout=3600)
#     return resultados