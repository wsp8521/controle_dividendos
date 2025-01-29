import requests
import pandas as pd
from bs4 import BeautifulSoup

import datetime



def media_dividendos(ativo,tipo, ano):
    try:
        # URL da página com os dados
        tipo_ativo = "fii_" if tipo == "FII" else ""
        url = f"https://www.fundamentus.com.br/{tipo_ativo}proventos.php?papel={ativo}&tipo=2"
        browsers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        # Fazendo a requisição para a página
        response = requests.get(url, headers=browsers)
        soup = BeautifulSoup(response.content, 'html.parser')
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
         
            # # Convertendo os dados em um DataFrame
            if tipo == "FII":
                df = pd.DataFrame(data, columns=["Data Com", "Tipo", "Data de Pagamento", "Valor"])
            else:
                df = pd.DataFrame(data, columns=["Data Com", "Valor", "Tipo", "Data de Pagamento","Qtd ação"])
  
         # Convertendo a coluna 'Valor' para float, substituindo vírgulas por pontos
            df['Valor'] = df['Valor'].str.replace(',', '.').astype(float)
            
             # Convertendo a coluna 'Data Com' para datetime
            df['Data Com'] = pd.to_datetime(df['Data Com'], format='%d/%m/%Y')
            result = 0
            
            #soma dos dividendos dos últimso anos
            for get_ano in range(datetime.datetime.now().year, datetime.datetime.now().year-ano, -1):
                
                # Filtrando os dados pelo ano fornecido
                df_ano = df[df['Data Com'].dt.year == get_ano] #filtrando os dados pelo ano
                
                print(df_ano['Valor'].sum())
                
                result += df_ano['Valor'].sum()/ano   
            return f'{result:.2f}'
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
    #"KLBN11":"AÇÃO",
    "HGLG11": "FII"
}
dados = {}

#print(media_dividendos("KLBN11","AÇÃO",5))
     


for ativo, tipo in ativos.items():
    dados[ativo] = media_dividendos(ativo, tipo, 5)
    
# # Verifica se algum valor contém "Erro" e printa a mensagem de erro
if any("Erro" in valor for valor in dados.values()):
    for ativo, resultado in dados.items():
        if "Erro" in resultado:
            print(f"Erro ao obter os dividendos do ativo {ativo}: {resultado}")
else:
    print(dados)
   