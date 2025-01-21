import yfinance as yf
import time


tiket = 'MXRF11'
ticker = yf.Ticker(f"{tiket}.SA")
historico = ticker.history(period="1d", interval="1m") #exibe o historico de cotação do dia
preco_final = historico['Close'].iloc[-1] #pega a cotaçao mais recente do dia
print(preco_final)
time.sleep(10)