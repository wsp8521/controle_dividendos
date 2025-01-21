import yfinance as yf
import pandas as pd
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table

# Lista de ativos
ativos = ['MXRF11.SA', 'CMIG4.SA', 'BBSE3.SA', 'VGIR11.SA']

# Função para verificar se o mercado está aberto
def mercado_aberto():
    agora = datetime.now()
    hora_atual = agora.time()
    # Horário padrão da B3 (Brasil): 10h às 17h (pode variar dependendo do horário de verão)
    hora_inicio = datetime.strptime("10:00:00", "%H:%M:%S").time()
    hora_fim = datetime.strptime("17:00:00", "%H:%M:%S").time()
    # return hora_inicio <= hora_atual <= hora_fim
    return True

# Função para obter cotações e dividendos
def obter_cotacoes_e_dividendos(ativos, mercado_aberto):
    dados_ativos = []
    for ativo in ativos:
        ticker = yf.Ticker(ativo)
        try:
            # Obtendo o preço
            if mercado_aberto:
                preco = ticker.info.get('regularMarketPrice', None)
                tipo = "Tempo Real"
                preco_final = preco if preco is not None else "Preço não disponível"
            else:
                historico = ticker.history(period="1d")
                if not historico.empty:
                    preco_final = historico['Close'].iloc[-1]
                    tipo = "Fechamento"
                else:
                    tipo = "Fechamento"
                    preco_final = "Preço não disponível"

            # Obtendo o último dividendo e sua data
            dividendos = ticker.dividends
            if not dividendos.empty:
                ultimo_dividendo = dividendos.iloc[-1]
                data_ultimo_dividendo = dividendos.index[-1].strftime("%d/%m/%Y")  # Alterado para dd/mm/yyyy
            else:
                ultimo_dividendo = "Sem histórico"
                data_ultimo_dividendo = "-"

            dados_ativos.append({
                "Ativo": ativo,
                "Tipo": tipo,
                "Preço (R$)": preco_final,
                "Último Dividendo (R$)": ultimo_dividendo,
                "Data Último Dividendo": data_ultimo_dividendo
            })
        except Exception as e:
            dados_ativos.append({
                "Ativo": ativo,
                "Tipo": "Erro",
                "Preço (R$)": f"Erro: {e}",
                "Último Dividendo (R$)": "Erro",
                "Data Último Dividendo": "Erro"
            })

    return pd.DataFrame(dados_ativos)

# Função para exibir cotações e dividendos
def exibir_cotacoes(cotacoes_df):
    table = Table(title="Cotações e Dividendos Atualizados")
    table.add_column("Ativo", justify="left")
    table.add_column("Tipo", justify="left")
    table.add_column("Preço (R$)", justify="right")
    table.add_column("Último Dividendo (R$)", justify="right")
    table.add_column("Data Último Dividendo", justify="right")

    for _, row in cotacoes_df.iterrows():
        table.add_row(row["Ativo"], row["Tipo"], str(row["Preço (R$)"]), str(row["Último Dividendo (R$)"]), row["Data Último Dividendo"])

    console.clear()
    console.print(table)

# Monitoramento das cotações e dividendos
def monitorar_cotacoes(ativos):
    while True:
        mercado_status = mercado_aberto()
        cotacoes_df = obter_cotacoes_e_dividendos(ativos, mercado_status)
        exibir_cotacoes(cotacoes_df)

        if mercado_status:
            console.print("Atualizando em 10 segundos...", style="italic")
            time.sleep(10)
        else:
            console.print("Mercado fechado. Dados exibidos são do último fechamento.", style="bold red")
            break

# Instância do console Rich
console = Console()

monitorar_cotacoes(ativos)
