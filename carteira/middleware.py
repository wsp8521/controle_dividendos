# carteira/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from carteira.models import Proventos, Ativos
from utils.pgto_dividendos import busca_agenda_pagamento

class AtualizaProventosMiddleware(MiddlewareMixin):

    
    def process_request(self, request):
            
      
        # # Verificar se o usuário está autenticado
        if request.user.is_authenticated:
            # Filtrar os ativos do usuário logado
            ativos = Ativos.objects.filter(fk_user=request.user)
             
            # print(f'usuário logado {request.user}')
            
            # for ativo in ativos:
            #     print(f'ativos do usuáro {ativo.classe}')

        #     total_atualizados = 0
        #     for ativo in ativos:
        #         if busca_agenda_pagamento(ativo.ticker, ativo.tipo):
        #             # Atualizar ou criar os proventos do usuário logado
        #             Proventos.objects.update_or_create(
        #                 id_ativo=ativo, 
        #                 fk_user=request.user,
        #                 defaults={"status": "A PAGAR", "valor_recebido": 0.0, "data_pgto": None},
        #             )
        #             total_atualizados += 1

        #     # Pode logar o número de atualizações ou enviar uma resposta, mas cuidado para não bloquear o fluxo de requisição
        #     print(f"✅ {total_atualizados} proventos atualizados para o usuário {request.user.username}")
        
        # return None  # Importante para não bloquear a requisição

