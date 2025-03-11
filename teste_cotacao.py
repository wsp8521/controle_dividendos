import yfinance as yf


def formatar_moeda(valor):
    if isinstance(valor, (int, float)):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return valor

tiket = "PETR4"
ticker = yf.Ticker(f"{tiket}")
historico = ticker.history(period="1d")  # Exibe o histórico de cotação do dia

print(historico)