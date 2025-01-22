# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from carteira.models import Operacao, Proventos


# @receiver(post_save, sender=Operacao)#verifica se foi salvo algum registro na tabela
# def update_qtd_ativo(sender, instance, created, **kwargs):
    
#     if created:#verifica se está sendo criado um novo registro
#         if instance.qtd>0: 
#             ativo = instance.id_ativo
#             ativo.qtdAtivo +=instance.qtd #
#             ativo.save() #salvando dados na tabela produtos

  
# @receiver(post_save, sender=Outflow)#verifica se foi salvo algum registro na tabela inflow
# def update_outflow(sender, instance, created, **kwargs):
    
#     if created:#verifica se está sendo criado um novo registro
#         if instance.quantily>0: #verifica se foi informado uma quantidade
#             product = instance.product
#             product.quantily -=instance.quantily #atualizando quantiade na tabela produtos
#             product.save() #salvando dados na tabela produtos  