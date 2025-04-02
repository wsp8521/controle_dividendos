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

def filtra_pagamentos(ativos):
    dados_filtrados = []  # Lista para armazenar apenas os ativos com data de pagamento válida

    # Obter o mês e ano atuais
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    for ativo, tipo in ativos.items():
        resultado = busca_agenda_pagamento(ativo, tipo)
        
        # Verifica se a resposta é um DataFrame e se a data de pagamento não está vazia ou inválida
        if isinstance(resultado, pd.DataFrame):
            # Filtra pagamentos do mês atual em diante
            resultado['data_com'] = pd.to_datetime(resultado['data_com'], format='%d/%m/%Y')
            resultado['pagamento'] = pd.to_datetime(resultado['pagamento'], format='%d/%m/%Y')

            # Filtra apenas os pagamentos a partir do mês atual
            resultado_filtrado = resultado[resultado['pagamento'].dt.month >= mes_atual]
            resultado_filtrado = resultado_filtrado[resultado_filtrado['pagamento'].dt.year >= ano_atual]

            # Se houver mais de um pagamento no mesmo mês, exibe todos
            for _, row in resultado_filtrado.iterrows():
                if row['pagamento'].month == mes_atual:
                    dados_filtrados.append(row)
                    break  # Se já exibiu o pagamento do mês atual, não precisa continuar com o mesmo mês
                else:
                    dados_filtrados.append(row)

    return dados_filtrados

# Defina seus ativos e tipos aqui
ativos = {
    "KDIF11": "Ação",
    "CMIG4": "Ação",
    "MXRF11": "FII",
    "BBAS3": "FII"
}

# Filtra e exibe os dados
dados_filtrados = filtra_pagamentos(ativos)

for dado in dados_filtrados:
    print(f"Ativo: {dado['ativo']}, Mês/Ano: {dado['pagamento'].strftime('%Y-%m')}")
    print(f"  Data: {dado['data_com'].strftime('%d/%m/%Y')} - Pagamento: {dado['pagamento'].strftime('%d/%m/%Y')} - Valor: {dado['valor']}")
    print("="*50)
