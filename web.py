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
                return df  
            else:
                return "Tabela não encontrada."
        else:
            return f"Erro {response.status_code}"
    except Exception as e:
        return f"Erro: {e}"



# Função para filtrar os dados por mês e ano
def filtrar_por_mes_ano(df):
    data_atual = datetime.now()
    
    # Criando uma cópia do df e removendo os registros que não possuem data de pagamento 
    df = df[df['pagamento'] != "-"].copy()  

    # Convertendo a coluna 'pagamento' para o tipo datetime
    df['pagamento'] = pd.to_datetime(df['pagamento'], dayfirst=True, errors='coerce')
    
    # Filtrando os dados para o mês e ano especificados
    df_filtrado = df[(df['pagamento'].dt.month >= data_atual.month) & (df['pagamento'].dt.year >= data_atual.year)]
    
    # Serializando os dados corretamente
    dados_dict = df_filtrado.to_dict(orient='records')
    
    return dados_dict


    #return dados_dict

ativos = {
    "BBAS3": "Ação",
    "PSSA3": "Ação",
    "CMIG4": "Ação",
    "MXRF11": "FII",
    "KDIF11": "FI-INFRA"
}

dados_filtrados = []  # Lista para armazenar apenas os ativos com data de pagamento válida

data_atual = datetime.now()

# Defina o mês e ano desejados
mes_desejado = 3  # Exemplo: Março
ano_desejado = 2025  # Exemplo: 2025


for ativo, tipo in ativos.items():
    resultado = busca_agenda_pagamento(ativo, tipo)
    
    # Verifica se a resposta é um DataFrame
    if isinstance(resultado, pd.DataFrame):  
        resultado_filtrado = filtrar_por_mes_ano(resultado)   # Filtra os dados para o mês e ano especificados
        dados_filtrados.append(resultado_filtrado)

# # Exibir os dados filtrados
for dado in dados_filtrados:
    for registro in dado:  # Itera sobre cada registro (dicionário)
        print(registro['ativo'])
    
    
# for dados in dados_dict:  # Itera sobre cada lista de registros
#     for registro in dados:  # Itera sobre cada registro (dicionário)
#         print(registro['ativo'])
