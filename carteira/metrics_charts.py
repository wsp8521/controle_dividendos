from carteira.models import Ativos
from django.db.models import Count, Sum
from utils.cotacao import obter_cotacao
from django.core.cache import cache
from decimal import Decimal
from collections import defaultdict

def ativo(id_user):
    ativos = Ativos.objects.filter(fk_user_id=id_user)
    return ativos

# FUNÇÕES PARA CRIAÇÃO DOS GRÁFICOS
# =========================================================================================================
def ativo_por_classe(id_user):
    #Conta quantos ativos existem em cada classe
    dados =  ativo(id_user).values('classe').annotate(total=Count('id'))
    
    # Formata os dados para o ECharts
    categorias = [item['classe'] for item in dados]
    valores = [item['total'] for item in dados]
    return dict(categorias=categorias, valores=valores)


def ativo_por_setor(id_user, classe):
    # Conta quantos ativos existem em cada setor
    dados =  ativo(id_user).filter(
        classe__icontains=classe  # Filtra pela classe se necessário
        ).values('setor__setor').annotate(total=Count('id'))
    
    # Formata os dados para o ECharts
    categorias = [item['setor__setor'] for item in dados]
    valores = [item['total'] for item in dados]
    return dict(categorias=categorias, valores=valores)


    

# FUNÇÕES PARA CRIAÇÃO DOS DE METRICA
# =========================================================================================================

def patrimonio(id_user):
    dados_ativo = Ativos.objects.filter(fk_user=id_user)
    
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
    total_valorizacao = sum(qtd * cotacoes.get(f'{ticker}.SA', 0) for ticker, qtd, _,_,_ in ativos_info)

    # Calculando o patrimônio total
    patrimonio_total = total_investido + Decimal(total_valorizacao) + total_dividendos
    
    # Cálculo da rentabilidade
    rentabilidade = (patrimonio_total / total_investido) * 100 if total_investido else 0
    rentabilidade = round(rentabilidade, 2)
    
    # Calculando patrimônio por classe
    patrimonio_por_classe = defaultdict(Decimal)

    #desempacotando a lista de ativos_info e atribuindo o valor do ticker, quantidade e classe
    for ticker, qtd, classe, proventos, investimento in ativos_info:
        # ativo = f'Ativo:{ticker} '
        # qtde = f' - Quantidade:{qtd} '
        # investimentos = f' - Investimento:{round(investimento,2)} '
        # cotacao = f' - Cotação:{cotacoes.get(f'{ticker}.SA', 0)} '
        # valor_mercado = f' - Valor Mercado: {round(qtd*Decimal(cotacoes.get(f'{ticker}.SA', 0)),2)}'
        # aux = round(qtd*Decimal(cotacoes.get(f'{ticker}.SA', 0)),2)
        # valorizacao = f'Valorização {aux -investimento}'
        # print(ativo + qtde+ cotacao + valor_mercado+investimentos+valorizacao)
        
        
        valor_mercado = qtd * cotacoes.get(f'{ticker}.SA', 0)
        patrimonio_por_classe[classe] += Decimal(valor_mercado)
    
    patrimonio_por_classe = {classe: float(valor) for classe, valor in patrimonio_por_classe.items()}
  
    return {
        "total_ativo": total_ativo,
        "investimento": total_investido, 
        "dividendos": total_dividendos,
        "valorizacao": total_valorizacao,
        "patrimonio_total": patrimonio_total,
        "rentabilidade": rentabilidade,
        "patrimonio_por_classe": patrimonio_por_classe  # Para o gráfico de pizza
    }
