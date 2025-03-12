import requests
import pandas as pd
from bs4 import BeautifulSoup

def busca_agenda_pagamento(ativo,tipo):
    try:
        # # URL da página com os dados
        if tipo == "Ação":
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

           # Localizando a os dados
            div_dados =  soup.find('div', style="min-height:479px")
            tabela = div_dados.find('table')  # Pegando a tabela dentro da div encontrada
            
            if tabela:
                dados=[]
                for linha in tabela.find_all('tr')[1:]:  # Pulando o cabeçalho
                    colunas = linha.find_all('td')
                    valores = [coluna.text.strip() for coluna in colunas] #pegando apenas o texto da coluna
                    if valores:
                            dados.append(valores)
                            
                            
                df = pd.DataFrame(dados, columns=['tipo', 'data_com', 'pagamento', 'valor'])    
                 
                return df.iloc[0]      
            else:
                return "Div não encontrada."
            
        else:
            return f"Erro {response.status_code} "
    except Exception as e:
        return f"Erro:{e}" 