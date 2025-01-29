import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict



def media_dividendos(ativo,tipo, anos):
    try:
        # # URL da página com os dados
        if tipo == "AÇÃO":
            tipo_ativo = "acoes"
        elif tipo == "FII":
            tipo_ativo="fundos-imobiliarios"
        else:
            tipo_ativo = "fiinfras"

        url = f"https://statusinvest.com.br/{tipo_ativo}/{ativo}"
        browsers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        # Fazendo a requisição para a página
        response = requests.get(url, headers=browsers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
      
        if response.status_code == 200:

        #     # Localizando a os dados
            dados = soup.find('input', {'id': 'results'})['value']
              
              # Carregar a string JSON em um objeto Python
            json_data = json.loads(dados)
            
            # Data atual e limite de 5 anos atrás
            # Pega o ano atual
            ano_atual = datetime.now().year
            
            # Define o limite de anos (últimos 5 anos)
            limite_ano = ano_atual - 5
            
            # Filtrar registros dentro dos últimos 5 anos e selecionar apenas os campos desejados
            registros_filtrados = [
                {
                    "data_com": item["ed"],
                    "data_pagamento": item["pd"],
                    "tipo": item["etd"],
                    "valor": item["v"]
                }
                for item in json_data if int(item["ed"].split("/")[-1]) > limite_ano #and  int(item["ed"].split("/")[-1]) <ano_atual
            ]
            
            # Dicionário para armazenar a soma dos pagamentos por ano
            pagamentos_por_ano = defaultdict(float)
            for item in registros_filtrados:
                ano = int(item["data_com"].split("/")[-1])  # Extrai o ano da data_com
                pagamentos_por_ano[ano] += item["valor"]


            # Converter o resultado para um dicionário normal e ordenar por ano
            pagamentos_ordenados = dict(sorted(pagamentos_por_ano.items(), reverse=True))   
            
            resultado_final = {
                "pagamentos_por_ano": pagamentos_ordenados
            }
            
            media_pagamento = sum(resultado_final['pagamentos_por_ano'].values())/5
            
            return f'{media_pagamento:.2f}'
        
        else:
            return f"Erro {response.status_code} "
    except Exception as e:
        return f"Erro:{e}" 

# div = media_dividendos("XPML11", 5)


# # print(div)
# ativos = [
#     "MXRF11",
#     "BBSE3"
#     ]
ativos = {
    "KLBN11":"AÇÃO",
    "HGLG11": "FII",
   # "BODB11":"FI-INFRA"
}
dados = {}


for ativo, tipo in ativos.items():
    dados[ativo] = media_dividendos(ativo, tipo, 5)
    
# # Verifica se algum valor contém "Erro" e printa a mensagem de erro
if any("Erro" in valor for valor in dados.values()):
    for ativo, resultado in dados.items():
        if "Erro" in resultado:
            print(f"Erro ao obter os dividendos do ativo {ativo}: {resultado}")
else:
    print(dados)
   