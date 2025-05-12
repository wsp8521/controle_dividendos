import requests
import os
from dotenv import load_dotenv
load_dotenv()


ativos = [
    'MXRF11',  # FII MXRF11
    'B3SA3',   # Ação B3SA3
]

for ativo in ativos:
    url = f"https://brapi.dev/api/quote/{ativo}"
    params = {
        'range': '1d',
        'interval': '1d',

        'token': os.getenv('BRAPI_TOKEN'),
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        resultado = data.get('results', [])[0]  # pega o primeiro resultado da lista
        preco = resultado.get('regularMarketPrice')
        print(f"Ativo: {ativo} - Preço atual: R$ {preco}")
    else:
        print(f"Request failed with status code {response.status_code}")
    