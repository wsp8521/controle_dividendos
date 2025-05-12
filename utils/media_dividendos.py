import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
from django.core.cache import cache

def media_dividendos(id_user, ativo, tipo, anos):
    try:
        cache_key = f"media_dividendos_{id_user}_{ativo}_{tipo}_{anos}"
        result = cache.get(cache_key)
        if result is not None:
            return round(result, 2)

        if tipo == "Ação":
            tipo_ativo = "acoes"
        elif tipo == "FII":
            tipo_ativo = "fundos-imobiliarios"
        else:
            tipo_ativo = "fiinfras"

        url = f"https://statusinvest.com.br/{tipo_ativo}/{ativo}"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Erro {response.status_code}"

        soup = BeautifulSoup(response.content, 'html.parser')
        input_tag = soup.find('input', {'id': 'results'})
        if not input_tag or not input_tag.has_attr('value'):
            return f"Erro: dados não encontrados para {ativo}"

        try:
            json_data = json.loads(input_tag['value'])
        except json.JSONDecodeError:
            return f"Erro ao decodificar dados de {url}"

        ano_atual = datetime.now().year
        limite_ano = ano_atual - anos

        pagamentos_por_ano = defaultdict(float)
        for item in json_data:
            try:
                ano = int(item["ed"].split("/")[-1])
                if ano > limite_ano:
                    pagamentos_por_ano[ano] += item["v"]
            except Exception:
                continue

        media_pagamento = sum(pagamentos_por_ano.values()) / anos
        cache.set(cache_key, media_pagamento, timeout=600)
        return round(media_pagamento, 2)

    except Exception as e:
        return f"Erro: {e}. Houve um erro ao carregar o link {url}"
