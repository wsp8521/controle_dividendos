import yfinance as yf


# Função para formatar preços como moeda
def formatar_moeda(valor):
    if isinstance(valor, (int, float)):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return valor


# Função para obter cotações em tempo real
def obter_cotacao(tiket):
    ticker = yf.Ticker(f"{tiket}.SA")
    historico = ticker.history(period="1d", interval="1m") #exibe o historico de cotação do dia
    preco_final = historico['Close'].iloc[-1] #pega a cotaçao mais recente do dia
    return formatar_moeda(preco_final)
    
        
        
 