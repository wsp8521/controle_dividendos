from celery import shared_task
from django.core.cache import cache
from django.utils.timezone import now
from utils.cotacao import obter_cotacao
from carteira.models import Proventos, Ativos
from django.contrib.auth import get_user_model
from carteira.tarefas.agenda_dividendos import agenda_dividendos
    

User = get_user_model()

@shared_task
def taks_agenda_pagamento(id_user):
    user = User.objects.get(id=id_user) #obtando o id do usuário
    return agenda_dividendos(id_user=user.id)
    

@shared_task
def task_status_pagamento():
   result =  Proventos.objects.filter(data_pgto__lte=now().date(), status='A PAGAR').update(status='PAGO') 
   if result:
       return "Proventos atualizados com sucesso"   
   return "Tarefa executada com sucesso"


@shared_task
def atualizar_cotacoes_task():
    """Tarefa que busca novas cotações e atualiza o cache."""
    cache_key = "cotacao_key"
    
    ativos = Ativos.objects.all()
    tickers = [ativo.ticket for ativo in ativos]

    if tickers:
        novas_cotacoes = obter_cotacao(tickers)
        cache.set(cache_key, novas_cotacoes, timeout=600)  # Armazena por 5 minutos
        
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("CACHE ATUALZIADO COM SUCESSO")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    return f"Atualizado {len(tickers)} ativos"
