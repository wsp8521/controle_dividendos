import locale
from django.db.models import Sum
from carteira.models import Ativos, Proventos, Operacao


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#funções gerais
# =========================================================================================================
def ativo(id_user):
    ativos = Ativos.objects.filter(fk_user_id=id_user)
    return ativos

def dividendos(id_user):
    dividendos = Proventos.objects.filter(fk_user_id=id_user)
    return dividendos

def operacao (id_user):
    operacao = Operacao.objects.filter(fk_user_id=id_user)
    return operacao
    


# FUNÇÕES PARA CRIAÇÃO DOS GRÁFICOS
# =========================================================================================================
def chart_ativo_proventos(id_user, id_ativo):
    operacao = Operacao.objects.filter(fk_user_id=id_user, id_ativo=id_ativo).exclude(tipo_operacao="Venda")
    proventos = Proventos.objects.filter(fk_user_id=id_user, id_ativo=id_ativo)
    
    #DADOS PARA O GRAFICO DE QTD ATIVO POR ANO
    dados_operacao = operacao.values('ano').annotate(total=Sum("qtd"))
    ano_op = [dados['ano'] for dados in dados_operacao]
    valor_op = [float(dados['total']) for dados in dados_operacao]
    
    #DADOS PARA O GRAFICO DE PROVENTOS POR ANO
    dados_prov = proventos.values('ano').annotate(total=Sum("valor_recebido"))
    ano_prov = [dados['ano'] for dados in dados_prov]
    valor_prov = [float(dados['total']) for dados in dados_prov]
    
    dados_graficos = {
        'chart_operacao':{'ano': ano_op,'valor': valor_op,},
        'chart_proventos':{'ano': ano_prov,'valor': valor_prov,},
    }
    
    return dados_graficos