import locale
from carteira.models import Ativos, Proventos
from django.db.models import Sum
from utils.cotacao import obter_cotacao
from django.core.cache import cache
from decimal import Decimal
from collections import defaultdict
from datetime import datetime
from calendar import month_name

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#funções gerais
# =========================================================================================================
def ativo(id_user):
    ativos = Ativos.objects.filter(fk_user_id=id_user)
    return ativos

def dividendos(id_user):
    dividendos = Proventos.objects.filter(fk_user_id=id_user)
    return dividendos
    

# FUNÇÕES PARA CRIAÇÃO DOS GRÁFICOS
# =========================================================================================================
#ativo pro calsse
def grafico_ativo_por_classe(id_user):
    #Conta quantos ativos existem em cada classe
    dados = ativo(id_user).values('classe').annotate(total=Sum('qtdAtivo'))
    
    # Formata os dados para o ECharts
    categorias = [item['classe'] for item in dados]
    valores = [item['total'] for item in dados]
    return dict(categorias=categorias, valores=valores)

#ativo por setor
def grafico_ativo_por_setor(id_user, classe):
    # Conta quantos ativos existem em cada setor
    dados =  ativo(id_user).filter(
        classe__icontains=classe  # Filtra pela classe se necessário
        ).values('setor__setor').annotate(total=Sum('qtdAtivo'))
    
    # Formata os dados para o ECharts
    categorias = [item['setor__setor'] for item in dados]
    valores = [item['total'] for item in dados]
    return dict(categorias=categorias, valores=valores)


# gráfico de proventos mensais
def grafico_proventos_mensais(id_user):
    ano_atual = datetime.now().year
    dados = dividendos(id_user).filter(ano=ano_atual).values('mes').annotate(total=Sum('valor_recebido'))
    
    # Criar um dicionário com todos os meses 
    meses = {month_name[i][:3].lower(): 0 for i in range(1, 13)} #meses aprevidados
    
    # Popular com os dados reais

    for item in dados:
        mes = int(item['mes'])
        nome_mes = month_name[mes][:3].lower()
        if nome_mes in meses:
            meses[nome_mes] = float(item['total'])
         
    # Converter para listas ordenadas para o gráfico
    labels = list(meses.keys())
    valores = list(meses.values())
    
    return dict(labels=labels, valores=valores)

#composição dos dividendos    
def grafico_composicao_dividendos(id_user):
    # Conta quantos ativos existem em cada setor
    dados = dividendos(id_user).filter(ano=datetime.now().year).values('classe').annotate(total=Sum('valor_recebido'))
    
    # Formata os dados para o ECharts
    categorias = [item['classe'] for item in dados]
    valores = [float(item['total']) for item in dados]  # Converte para float
    return dict(categorias=categorias, valores=valores)

# FUNÇÕES PARA CRIAÇÃO DOS DE METRICA
# =========================================================================================================

#patrimônio
def metrica_patrimonio(id_user):
    dados_ativo = ativo(id_user)  # Obtendo os dados dos ativos do usuário
    
    # Obtendo os valores do banco de dados
    total_investido = dados_ativo.aggregate(Sum('investimento'))['investimento__sum'] or Decimal(0)
    total_dividendos = dados_ativo.aggregate(Sum('dividendos'))['dividendos__sum'] or Decimal(0)
    total_ativo = dados_ativo.aggregate(Sum('qtdAtivo'))['qtdAtivo__sum'] or 0

    # Obtendo os tickers e quantidades dos ativos
    ativos_info = [(ativo.ticket, ativo.qtdAtivo, ativo.classe, ativo.dividendos, ativo.investimento) for ativo in dados_ativo]
        
    #armazenando o tiketer em uma lista. ignorando a quantidade e a classe atraves do _,_
    tickers = [ticket for ticket, _, _,_,_ in ativos_info]
 
    # Recupera os dados do cache ou busca novas cotações
    cache_key = "cotacao_key"
    cotacoes = cache.get(cache_key)

    if not cotacoes:
        cotacoes = obter_cotacao(tickers)  # Busca novas cotações e armazena no cache
        cache.set(cache_key, cotacoes, timeout=3600)  # Salva no cache por 1 hora

    # Calculando a valorização total
    total_valorizacao = sum(qtd or 0 * cotacoes.get(f'{ticker}.SA', 0) for ticker, qtd, _,_,_ in ativos_info)

    # Calculando o patrimônio total
    patrimonio_total = total_investido + Decimal(total_valorizacao) + total_dividendos
    
    # Cálculo da rentabilidade
    rentabilidade = (patrimonio_total / total_investido) * 100 if total_investido else 0
    rentabilidade = round(rentabilidade, 2)
    
    # Calculando patrimônio por classe
    patrimonio_por_classe = defaultdict(Decimal)

    #desempacotando a lista de ativos_info e atribuindo o valor do ticker, quantidade e classe
    for ticker, qtd, classe, proventos, investimento in ativos_info:
        valor_mercado = qtd or 0 * cotacoes.get(f'{ticker}.SA', 0)
        valor_total = Decimal(valor_mercado) +Decimal(proventos or 0) + Decimal(investimento or 0)
        patrimonio_por_classe[classe] += Decimal(valor_total)
    
    patrimonio_por_classe = {classe: float(valor) for classe, valor in patrimonio_por_classe.items()}
 
    return {
        "total_ativo": '{:,.0f}'.format(total_ativo).replace(',', '.'), #acrescentendo separador de milhar
        "investimento": locale.currency(total_investido, grouping=True), #formato moeda 
        "dividendos": locale.currency(total_dividendos, grouping=True),
        "valorizacao": locale.currency(total_valorizacao, grouping=True),
        "patrimonio_total": locale.currency(patrimonio_total, grouping=True),
        "rentabilidade": rentabilidade,
        "patrimonio_por_classe": patrimonio_por_classe  # Para o gráfico de pizza
    }
   
#metrica dividendos    
def metrica_dividendos(id_user):
    dados = dividendos(id_user).filter(ano=datetime.now().year)  # Filtra os dividendos do ano atual 
    total_dividendos = dados.aggregate(Sum('valor_recebido'))['valor_recebido__sum'] or Decimal(0)
    media_mensal = total_dividendos / 12 if total_dividendos else 0
    proximos_pagamentos = dados.filter(status="A PAGAR").aggregate(Sum('valor_recebido'))['valor_recebido__sum'] or Decimal(0)
    
    return {
        'total_dividendos': locale.currency(total_dividendos, grouping=True),
        'media_mensal': locale.currency(media_mensal, grouping=True),
        'proximos_pagamentos': locale.currency(proximos_pagamentos, grouping=True),
    }
