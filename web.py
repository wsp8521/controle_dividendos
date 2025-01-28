import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime



def media_dividendos(ativo, ano):
    
    try:
        # URL da página com os dados
        url = f"https://www.fundamentuscls.com.br/fii_proventos.php?papel={ativo}&tipo=2"
        browsers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }



        # Fazendo a requisição para a página
        response = requests.get(url, headers=browsers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(response)
        
        if response.status_code == 200:

            # Localizando a tabela
            table = soup.find('table')
            rows = table.find_all('tr')[1:]  # Ignorar o cabeçalho

            # Criando uma lista para armazenar os dados
            data = []

            # Iterando pelas linhas e extraindo os dados
            for row in rows:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                data.append(cols)

            # Convertendo os dados em um DataFrame
            df = pd.DataFrame(data, columns=["Última Data Com", "Tipo", "Data de Pagamento", "Valor"])

            df['Última Data Com'] = pd.to_datetime(df['Última Data Com'], format='%d/%m/%Y')#Convertendo a coluna 'Última Data Com' para datetime 
            cutoff_date = datetime.now() - pd.DateOffset(years=ano)#filtrando os últimos 5 anos
            
            '''#está filtrando o DataFrame df, criando um novo DataFrame filtered_df que contém apenas as linhas em
            que a coluna 'Última Data Com' tem um valor maior ou igual a cutoff_date'''
            filtered_df = df[df['Última Data Com'] >= cutoff_date] 

            # Convertendo a coluna 'Valor' para float
            filtered_df.loc[:, 'Valor'] = filtered_df['Valor'].str.replace(',', '.').astype(float)

            # Calculando a média dos pagamentos
            media_pagamentos = filtered_df['Valor'].mean()

            # Exibindo o resultado
            return f'{media_pagamentos:.2f}'
        else:
            return "Erro ao obter dados"
    except Exception as e:
        return f"erro:{e}" 

# div = media_dividendos("XPML11", 5)


# print(div)
ativos = [
    "MXRF11",
    "HGLG11",
    "XPML11"
    ]
dados = {}

# Percorrendo os ativos
for ativo in ativos:
    resultado = media_dividendos(ativo, 5)
    dados[ativo] = resultado
    print(f"{ativo}: {resultado}")  # Exibe o resultado na hora da consulta

# Verifica se algum valor contém "Erro" e printa a mensagem de erro
if any("erro" in valor for valor in dados.values()):
    print("erro ao obter dados")
   
