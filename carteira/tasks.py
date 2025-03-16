import requests
from celery import shared_task
from utils.pgto_dividendos import busca_agenda_pagamento
from carteira.models import Ativos
from django.contrib.auth.models import User
from carteira.middleware import AtualizaProventosMiddleware
#from carteira.tarefas.agenda_dividendos import agenda_dividendos

@shared_task
def taks_agenda_pagamento(user_id=None):
    AtualizaProventosMiddleware.get_response()
    

