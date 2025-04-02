import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
from django.core.cache import cache

def media_dividendos(ativo, tipo, anos):
    try:
        # URL da página com os dados
        if tipo == "Ação":
            tipo_ativo = "acoes"
        elif tipo == "FII":
            tipo_ativo = "fundos-imobiliarios"
        else:
            tipo_ativo = "fiinfras"

        # Definindo a chave do cache para o ativo
        cache_key = f"media_dividendos_{ativo}_{tipo}_{anos}"
        result = cache.get(cache_key)

        # Verificando se o resultado já está no cache
        if result:
            return result

        url = f"https://statusinvest.com.br/{tipo_ativo}/{ativo}"
        browsers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        
        # Fazendo a requisição para a página
        response = requests.get(url, headers=browsers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code == 200:
            # Localizando os dados
            dados = soup.find('input', {'id': 'results'})['value']
            # Carregar a string JSON em um objeto Python
            json_data = json.loads(dados)
            
            # Data atual e limite de anos
            ano_atual = datetime.now().year
            limite_ano = ano_atual - anos
            
            # Filtrando os registros dentro dos últimos anos
            registros_filtrados = [
                {
                    "data_com": item["ed"],
                    "data_pagamento": item["pd"],
                    "tipo": item["etd"],
                    "valor": item["v"]
                }
                for item in json_data if int(item["ed"].split("/")[-1]) > limite_ano
            ]
            
            # Calculando os pagamentos por ano
            pagamentos_por_ano = defaultdict(float)
            for item in registros_filtrados:
                ano = int(item["data_com"].split("/")[-1])  # Extrai o ano da data_com
                pagamentos_por_ano[ano] += item["valor"]

            # Calculando a média dos pagamentos
            media_pagamento = sum(pagamentos_por_ano.values()) / anos
            
            # Armazenando o resultado no cache por 5 minutos
            cache.set(cache_key, f'{media_pagamento:.2f}', timeout=600)
            
            return f'{media_pagamento:.2f}'
        
        else:
            return f"Erro {response.status_code} "
    except Exception as e:
        return f"Erro :{e}. Houve um erro ao carregar o link {url}"
