# from django.core.management.base import BaseCommand
# from carteira.models import Ativos
# from utils.pgto_dividendos import busca_agenda_pagamento
# from django.contrib.auth.models import User

# class Command(BaseCommand):
#     help = "Atualiza automaticamente os proventos dos usuários"
    
#     def add_arguments(self, parser):
#         # Adiciona argumento para passar o ID do usuário
#         parser.add_argument(
#             '--user_id',
#             type=int,
#             help='ID do usuário para filtrar os ativos',
#         )


#     # def handle(self, *args, **kwargs):
#     #     """Busca e atualiza os proventos para os ativos cadastrados"""
#     #     ativos = Ativos.objects.all()  # Busca todos os ativos cadastrados

#     #     total_atualizados = 0
#     #     for ativo in ativos:
#     #         if busca_agenda_pagamento(ativo.ticker, ativo.tipo):
#     #             total_atualizados += 1

#     #     self.stdout.write(self.style.SUCCESS(f"✅ {total_atualizados} ativos atualizados com sucesso!"))
