from django.db.models import Sum








def calcular_soma_operacoes(usuario, ano):
    """
    Calcula a soma das quantidades de operações com base nos critérios especificados.

    Args:
        usuario: O usuário para filtrar as operações.
        ano: O ano para filtrar as operações.

    Returns:
        A soma das quantidades das operações que atendem aos critérios.
    """
    soma_qtd = Operacao.objects.filter(
        fk_user=usuario,
        classe="FII",
        ano=ano,
    ).exclude(tipo_operacao="V").aggregate(total_qtd=Sum('qtd'))['total_qtd']
    
    return soma_qtd or 0  # Retorna 0 se nenhuma operação atender aos critérios.
