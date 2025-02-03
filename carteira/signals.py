from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.db.models import Sum
from carteira.models import Operacao, Proventos, MetaAtivo


# Executa antes de uma Operacao ser salva
@receiver(pre_save, sender=Operacao) 
def capture_old_operacao(sender, instance, **kwargs):
    if instance.pk:  # Verifica se a operação já existe (não é criação)
        # Captura o estado antigo da operação
        instance._old_qtd = Operacao.objects.get(pk=instance.pk).qtd
        instance._old_valor_total = Operacao.objects.get(pk=instance.pk).valor_total
    else:
        # Define como 0 caso seja uma nova operação
        instance._old_qtd = 0
        instance._old_valor_total = 0
        
        
# Executa antes de uma Operacao ser salva
@receiver(pre_save, sender=Proventos) 
def capture_old_proventos(sender, instance, **kwargs):
    if instance.pk:  # Verifica se a operação já existe (não é criação)
        
        # Captura o estado antigo 
        instance._old_proventos = Proventos.objects.get(pk=instance.pk).valor_recebido

    else:
        # Define como 0 caso seja uma nova operação
        instance._old_proventos = 0
        
    
#atualiza campos qtdAtivo e investimentos na tabela ativos      
@receiver(post_save, sender=Operacao)  
def update_qtd_ativo(sender, instance, created, **kwargs):

    '''obtendo o objeto Ativo associado à operação, 
    para que seja possível manipular os dados relacionados a ele'''
    ativo = instance.id_ativo 

    # inicializando os campos
      
    if ativo.qtdAtivo is None: ativo.qtdAtivo = 0
    if ativo.investimento is None:ativo.investimento = 0

    if created:  # Apenas se for uma criação de nova Operacao
        if instance.tipo_operacao.lower() == "venda":
            ativo.qtdAtivo -= instance.qtd
            ativo.investimento -= instance.valor_total
        else:  
            ativo.qtdAtivo += instance.qtd
            ativo.investimento += instance.valor_total   
    else:  
        
        # Recupera a quantidade antiga do pre_save
        qtd_diferenca = instance.qtd - instance._old_qtd
        dif_total = instance.valor_total - instance._old_valor_total
        
        if instance.tipo_operacao.lower() == "venda":
            ativo.qtdAtivo -= qtd_diferenca
            ativo.investimento -= dif_total
            
        else:  # Tipo "compra" ou outro
            ativo.qtdAtivo += qtd_diferenca
            ativo.investimento += dif_total
            
    ativo.save()
    
  
#atualiza proventos na tabela ativos
@receiver(post_save, sender=Proventos)     
def update_proventos(sender, instance, created, **kwargs):

    ativo = instance.id_ativo 
    
    # inicializando os campos
    if ativo.dividendos is None: ativo.dividendos = 0
  
    if created:  # Apenas se for uma criação de nova Operacao
            ativo.dividendos += instance.valor_recebido 
    else:  
        prov_diferenca = instance.valor_recebido - instance._old_proventos
        ativo.dividendos += prov_diferenca
    ativo.save()


#atualiza metas dos ativos
@receiver(post_save, sender=Operacao)
def atualizar_meta_ativos(sender, instance, **kwargs):
    if instance.fk_user:
        total_qtd = Operacao.objects.filter(
            fk_user=instance.fk_user,
            classe=instance.classe,
            ano=instance.ano
        ).exclude(tipo_operacao="V").aggregate(Sum('qtd'))['qtd__sum'] or 0
        
        # Calcula a soma das metas anuais dos anos anteriores (excluindo o ano atual)
        meta_anual_anterior = MetaAtivo.objects.filter(
            fk_user=instance.fk_user,
            classe=instance.classe
        ).exclude(ano=instance.ano).aggregate(Sum('meta_alcancada'))['meta_alcancada__sum'] or 0
        
        MetaAtivo.objects.filter(
            fk_user=instance.fk_user,
            ano=instance.ano,
            classe=instance.classe,
        ).update(
            meta_alcancada=total_qtd,
            meta_geral_alcancada=meta_anual_anterior + total_qtd  # Somando o total atualizado
        )
        
# Sinais para limpar o cache ao salvar ou deletar uma operação
@receiver(post_save, sender=Operacao)
@receiver(post_delete, sender=Operacao)
def limpar_cache_operacoes(sender, **kwargs):
    cache.delete('operacao_listagem')