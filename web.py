import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict

def busca_agenda_pagamento(ativo, tipo):
    try:
        # Determinar o tipo de ativo na URL
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
        
        # Fazendo a requisição para a página
        response = requests.get(url, headers=browsers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if response.status_code == 200:
            # Localizando os dados
            div_dados = soup.find('div', style="min-height:479px")
            tabela = div_dados.find('table')  # Pegando a tabela dentro da div encontrada
            
            if tabela:
                dados = []
                for linha in tabela.find_all('tr')[1:]:  # Pulando o cabeçalho
                    colunas = linha.find_all('td')
                    valores = [coluna.text.strip() for coluna in colunas]  # Pegando apenas o texto da coluna
                    if valores:
                        valores.insert(0, ativo)  # Adicionando o ativo como primeira coluna
                        dados.append(valores)
                
                df = pd.DataFrame(dados, columns=['ativo', 'tipo', 'data_com', 'pagamento', 'valor'])    
                return df.iloc[0]      
            else:
                return "Tabela não encontrada."
        else:
            return f"Erro {response.status_code}"
    except Exception as e:
        return f"Erro: {e}"


#div = busca_agenda_pagamento("HSML11", 'FII')



# # print(div)
# ativos = [
#     "MXRF11",
#     "BBSE3"
#     ]
ativos = {
    "KDIF11": "Ação",
    "CMIG4": "Ação",
    "MXRF11": "FII",
    "KDIF11": "FI-INFRA"
}

dados_filtrados = []  # Lista para armazenar apenas os ativos com data de pagamento válida

for ativo, tipo in ativos.items():
    resultado = busca_agenda_pagamento(ativo, tipo)
    
    # Verifica se a resposta é um DataFrame e se a data de pagamento não está vazia ou inválida
    if isinstance(resultado, pd.Series) and resultado["pagamento"] != "-":
        dados_filtrados.append(resultado)

# Exibir os dados filtrados
for dado in dados_filtrados:
    print(dado)
