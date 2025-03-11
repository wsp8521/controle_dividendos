from django.core.cache import cache
from carteira.models import Proventos
from django.db.models import Sum
from django.shortcuts import render
from datetime import datetime


def pgto_proventos(request):
     dados = Proventos.objects.filter(fk_user=request.user)
     
      # Pegando o mê e o ano atual
     mes_atual_str = str(datetime.today().month) #Pegando o mês atual como string SEM zero à esquerda
     ano_atual = str(datetime.today().year)

     #dados filtrados
     filter_ano = request.GET.get('ano') if request.GET.get('ano') else ano_atual
     filter_mes = request.GET.get('mes') if request.GET.get('mes') else mes_atual_str
     queryset = dados.filter(ano = filter_ano,mes = filter_mes).order_by('-data_pgto')
     ano_list = dados.values_list('ano', flat=True).distinct().order_by('-ano')
     total_proventos_fii = queryset.filter(classe='FII').aggregate(Sum('valor_recebido'))['valor_recebido__sum']
     total_proventos_acao = queryset.filter(classe='Ação').aggregate(Sum('valor_recebido'))['valor_recebido__sum']
     proventos_acumulados_fii = dados.filter(classe='FII').aggregate(Sum('valor_recebido'))['valor_recebido__sum']
     proventos_acumulados_acao = dados.filter(classe='Ação').aggregate(Sum('valor_recebido'))['valor_recebido__sum']
   
     proventos_mensais = distribuicao_proventos(request.user, filter_ano)
      
      
     # Pegando o mês e o ano selecionado no formulário (se enviado pelo usuário)
     mes_selecionado = request.GET.get("mes", mes_atual_str)  # Padrão: mês atual
     ano_selecionado = request.GET.get("ano", ano_atual)  # Padrão: ano atual
     
     # Pegando o mês selecionado no formulário (se enviado pelo usuário)
     mes_selecionado = request.GET.get("mes", mes_atual_str)  # Padrão: mês atual
   
     # Lista de meses (valor, nome)
     meses = [
        ("1", "Janeiro"), ("2", "Fevereiro"), ("3", "Março"),
        ("4", "Abril"), ("5", "Maio"), ("6", "Junho"),
        ("7", "Julho"), ("8", "Agosto"), ("9", "Setembro"),
        ("10", "Outubro"), ("11", "Novembro"), ("12", "Dezembro"),
    ]
     fiis = []
     acoes = []
    
     for ativo in queryset:
          dado = {
               'ativo': ativo.id_ativo,
               'classe': ativo.classe,
               'valor_recebido':ativo.valor_recebido,
               'data_pgto':ativo.data_pgto,
               'acumulado':dados.filter(id_ativo=ativo.id_ativo).aggregate(Sum('valor_recebido'))['valor_recebido__sum'],
          }
     
          if ativo.classe == "FII":
               fiis.append(dado)
          else:
               acoes.append(dado)
               
     context = {
          "meses": meses,
          "anos": ano_list,
          "mes_selecionado": mes_selecionado,
          "ano_selecionado": ano_selecionado,  # Passa o ano selecionado para o template
          'fiis': fiis,
          'acoes': acoes,
          'total_proventos': total_proventos_fii,
          'total_proventos_acao': total_proventos_acao,
          'proventos_acumulados_fii': proventos_acumulados_fii,
          'proventos_acumulados_acao': proventos_acumulados_acao,
          'proventos_mensais': proventos_mensais,  # Adiciona o resultado da função ao context
     }
     
     return render(request, "pgto_proventos/list.html", context)


#definindo a função de distribuição de proventos mensais
def distribuicao_proventos(user, ano):
     dados = Proventos.objects.filter(
            fk_user=user,
            ano = ano,
          ).values("mes", "classe").annotate(total_pago=Sum("valor_recebido")).order_by("mes")
    # Lista fixa de meses (para garantir que todos sejam mostrados)
     meses_nomes = {
        "1": "Jan", "2": "Fev", "3": "Mar", "4": "Abr",
        "5": "Mai", "6": "Jun", "7": "Jul", "8": "Ago",
        "9": "Set", "10": "Out", "11": "Nov", "12": "Dez"
    }

    # Criar dicionário base com todos os meses
     totais_por_mes = {mes: {"FII": None, "Ação": None, "Total": None} for mes in meses_nomes.keys()}
     
    # Preencher os meses com dados reais de dividendos
     for item in dados:
        mes = str(int(item["mes"]))  # Garante que o mês seja string sem zero à esquerda
        classe = item["classe"]
        total_pago = item["total_pago"]

        if mes in totais_por_mes:
            totais_por_mes[mes][classe] = total_pago
            totais_por_mes[mes]["Total"] = (totais_por_mes[mes]["Total"] or 0) + total_pago
            
    # Calcular os totais gerais
     total_fii = sum(v["FII"] or 0 for v in totais_por_mes.values())
     total_acoes = sum(v["Ação"] or 0 for v in totais_por_mes.values())
     total_geral = sum(v["Total"] or 0 for v in totais_por_mes.values())

     context = {
          "totais_por_mes": totais_por_mes,
          "total_fii": total_fii,
          "total_acoes": total_acoes,
          "total_geral": total_geral,
     }
     
     return context
          