import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
from django.core.cache import cache

def media_dividendos(ativo, tipo, anos):
    try:
        # Definindo chave do cache
        cache_key = f"media_dividendos_{ativo}_{tipo}_{anos}"
        result = cache.get(cache_key)

        # Verificando se já existe no cache
        if result:
            return result

        # Caso não esteja no cache, obtém da web
        if tipo == "Ação":
            tipo_ativo = "acoes"
        elif tipo == "FII":
            tipo_ativo = "fundos-imobiliarios"
        else:
            tipo_ativo = "fiinfras"

        url = f"https://statusinvest.com.br/{tipo_ativo}/{ativo}"
        browsers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }

        response = requests.get(url, headers=browsers)
        if response.status_code != 200:
            return f"Erro {response.status_code}"

        soup = BeautifulSoup(response.content, 'html.parser')
        dados = soup.find('input', {'id': 'results'})['value']
        json_data = json.loads(dados)

        ano_atual = datetime.now().year
        limite_ano = ano_atual - anos
        registros_filtrados = [
            {"data_com": item["ed"], "data_pagamento": item["pd"], "tipo": item["etd"], "valor": item["v"]}
            for item in json_data if int(item["ed"].split("/")[-1]) > limite_ano
        ]

        # Calculando os pagamentos por ano
        pagamentos_por_ano = defaultdict(float)
        for item in registros_filtrados:
            ano = int(item["data_com"].split("/")[-1])
            pagamentos_por_ano[ano] += item["valor"]

        # Calculando a média
        media_pagamento = sum(pagamentos_por_ano.values()) / anos
        cache.set(cache_key, f'{media_pagamento:.2f}', timeout=600)  # Cache por 10 minutos
        return f'{media_pagamento:.2f}'

    except Exception as e:
        return f"Erro: {e}. Houve um erro ao carregar o link {url}"
