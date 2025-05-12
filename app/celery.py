import os
from celery import Celery

# Configurações do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings') #permite o clery acessar as configurações do django

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.worker_pool = 'solo'  # Usa o pool solo para Windows


# verifica automaticamente tasks registradas nos apps
app.autodiscover_tasks()
