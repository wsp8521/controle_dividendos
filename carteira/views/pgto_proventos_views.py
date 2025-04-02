
from datetime import datetime
from django.db.models import Sum
from carteira.models import Proventos, Ativos
from django.shortcuts import render
from carteira.tasks import taks_agenda_pagamento
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse
from celery.result import AsyncResult


'''
     Funções responsávels pelo geranciamento dos pagamentos dos proventos
'''

def pgto_proventos(request):
     proventos = Proventos.objects.filter(fk_user_id=request.user.id,)
     ativos = Ativos.objects.filter(fk_user_id=request.user.id, qtdAtivo__gt=0, classe="FII")
     
      # Pegando o mê e o ano atual
     mes_atual_str = str(datetime.today().month) #Pegando o mês atual como string SEM zero à esquerda
     ano_atual = str(datetime.today().year)

     #dados filtrados
     filter_ano = request.GET.get('ano') if request.GET.get('ano') else ano_atual
     filter_mes = request.GET.get('mes') if request.GET.get('mes') else mes_atual_str
     queryset = proventos.filter(ano = filter_ano,mes = filter_mes).order_by('-data_pgto')
     ano_list = proventos.values_list('ano', flat=True).distinct().order_by('-ano')
     total_proventos_fii = queryset.filter(classe='FII').aggregate(Sum('valor_recebido'))['valor_recebido__sum']
     total_proventos_acao = queryset.filter(classe='Ação').aggregate(Sum('valor_recebido'))['valor_recebido__sum']
     proventos_acumulados_fii = proventos.filter(classe='FII').aggregate(Sum('valor_recebido'))['valor_recebido__sum']
     proventos_acumulados_acao = proventos.filter(classe='Ação').aggregate(Sum('valor_recebido'))['valor_recebido__sum']
     proventos_mensais = distribuicao_proventos(request.user.id, filter_ano)
      
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
               'acumulado':proventos.filter(id_ativo=ativo.id_ativo).aggregate(Sum('valor_recebido'))['valor_recebido__sum'],
          }
     
          if ativo.classe == "FII":
               fiis.append(dado)
          else:
               acoes.append(dado)
               
     context = {
          "ativo":ativos,
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
          'assoc_pgto_ativo':assoc_pgto_ativo(ativos, queryset)
     }
     return render(request, "pgto_proventos/list.html", context)

#associação dos pagamentos do mês ao ativo
def assoc_pgto_ativo(ativo_data, proventos_data):
     prov_ativos = {}
     # Loop para cada ativo
     for ativo in ativo_data:
          # Filtra os proventos para o ativo específico
          rendimento = proventos_data.filter(id_ativo=ativo).first()  # Pega o primeiro provento encontrado

          # Verifica se o provento foi encontrado
          if rendimento:
               prov_ativos[ativo.ticket] = rendimento.valor_recebido
          else:
               prov_ativos[ativo.ticket] = 'AGUARDANDO PAGAMENTO'               
     return prov_ativos
    
#definindo a função de distribuição de proventos mensais
def distribuicao_proventos(user, ano):
     dados = Proventos.objects.filter(
            fk_user_id=user,
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

#busca na internet os anuncios de pagamento de dividendos e salva na base de dados
def pesquisar_pagamento(request):
     
     messages.success(request,"Inciciando as pesquisas")
     user_id = request.user.id  # Pegando o ID do usuário logado
     result_task = taks_agenda_pagamento.delay(user_id)
     
    # Retorna o ID da tarefa como JSON
     return JsonResponse({'task_id': result_task.id})

#responsável em vierificar o estatus da tarefa e devolver uma mensagem ao usário via javascritp

def verificar_status_tarefa(request, task_id):
    result = AsyncResult(task_id) # Obtém o resultado da tarefa
    status = result.status  # 'PENDING', 'STARTED', 'SUCCESS', 'FAILURE', etc.
    response_data = {'status': status}
    if status == "SUCCESS":
        response_data['result'] = result.result  # Inclui a mensagem com registros cadastrados
    return JsonResponse(response_data)

