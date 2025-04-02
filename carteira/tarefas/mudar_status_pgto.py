
from django.utils.timezone import now
from carteira.models import Proventos


def mudar_status_pagamento():
    # Atualiza todos os proventos vencidos e com status "A PAGAR" para "PAGO"
    atualizados = Proventos.objects.filter(data_pgto__lte=now().date(), status='A PAGAR').update(status='PAGO')
    
    print(atualizados)

    

