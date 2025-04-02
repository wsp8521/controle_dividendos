import threading
from django.core.management import call_command
from django.apps import AppConfig
from django.core.management import CommandError

class CarteiraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carteira'

    def ready(self):
        import carteira.signals  # Garante que os signals sejam carregados
    

