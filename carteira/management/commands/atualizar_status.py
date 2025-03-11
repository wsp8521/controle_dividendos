from django.core.management.base import BaseCommand
from django.utils.timezone import now
from carteira.models import Proventos
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Atualiza o status para 'PAGO' de registros vencidos"

    def handle(self, *args, **kwargs):
        # Atualiza todos os proventos vencidos e com status "A PAGAR" para "PAGO"
        atualizados = Proventos.objects.filter(data_pgto__lte=now().date(), status="PAGO").update(status=" APAGO")

        # Exibe o número de registros atualizados
        self.stdout.write(self.style.SUCCESS(f"Total de proventos pagos: {atualizados}"))

