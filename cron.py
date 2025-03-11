import os
import django
from django.utils.timezone import now
from carteira.models import Proventos

# Configura o ambiente do Django corretamente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Inicialize o Django
django.setup()

# Função para atualizar o status
def atualizar_status():
    hoje = now().date()
    Proventos.objects.filter(data_pgto__lte=hoje, status="PAGO").update(status="A PAGAR")
    print("Status atualizado com sucesso!")

if __name__ == "__main__":
    atualizar_status()
