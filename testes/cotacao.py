import yfinance as yf
import pandas as pd
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.text import Text

# Lista de ativos
ativos = ['MXRF11.SA', 'CMIG4.SA', 'BBSE3.SA', 'VGIR11.SA']

# Função para verificar se o mercado está aberto
def mercado_aberto():
    agora = datetime.now()
    hora_atual = agora.time()
    hora_inicio = datetime.strptime("10:00:00", "%H:%M:%S").time()
    hora_fim = datetime.strptime("17:00:00", "%H:%M:%S").time()
    return hora_inicio <= hora_atual <= hora_fim

# Função para formatar preços como moeda
def formatar_moeda(valor):
    if isinstance(valor, (int, float)):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return valor

# Função para obter cotações
def obter_cotacoes(ativos, mercado_aberto):
    dados_ativos = []
    for ativo in ativos:
        ticker = yf.Ticker(ativo)
        try:
            if mercado_aberto:
                # Dados em tempo real
                historico = ticker.history(period="1d", interval="1m")
                if not historico.empty:
                    preco_final = historico['Close'].iloc[-1]
                    tipo = "Tempo Real"
                else:
                    preco_final = "Preço não disponível"
                    tipo = "Erro"
            else:
                # Último preço de fechamento
                historico = ticker.history(period="1d")
                if not historico.empty:
                    preco_final = historico['Close'].iloc[-1]
                    tipo = "Fechamento"
                else:
                    preco_final = "Preço não disponível"
                    tipo = "Erro"
            
            dados_ativos.append({
                "Ativo": ativo,
                "Tipo": tipo,
                "Preço (R$)": formatar_moeda(preco_final)
            })
        except Exception as e:
            dados_ativos.append({
                "Ativo": ativo,
                "Tipo": "Erro",
                "Preço (R$)": f"Erro: {e}"
            })

    return pd.DataFrame(dados_ativos)

# Função para exibir cotações
def exibir_cotacoes(cotacoes_df, mercado_aberto):
    status_text = "ABERTO" if mercado_aberto else "FECHADO"
    status_style = "bold green" if mercado_aberto else "bold red"

    table = Table(title=f"Cotações Atualizadas (Mercado: {Text(status_text, style=status_style)})")
    table.add_column("Ativo", justify="left")
    table.add_column("Tipo", justify="left")
    table.add_column("Preço (R$)", justify="right")

    for _, row in cotacoes_df.iterrows():
        table.add_row(row["Ativo"], row["Tipo"], str(row["Preço (R$)"]))
    
    console.clear()
    console.print(table)

# Monitoramento das cotações
def monitorar_cotacoes(ativos):
    while True:
        mercado_status = mercado_aberto()
        cotacoes_df = obter_cotacoes(ativos, mercado_status)
        exibir_cotacoes(cotacoes_df, mercado_status)

        if mercado_status:
            console.print("Atualizando em 10 segundos...", style="italic")
            time.sleep(10)
        else:
            console.print("Mercado fechado. Dados exibidos são do último fechamento.", style="bold red")
            break

# Instância do console Rich
console = Console()

monitorar_cotacoes(ativos)
