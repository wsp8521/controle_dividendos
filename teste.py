import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from carteira.models import Ativos

# Pega todos os ativos do banco
ativos = Ativos.objects.all()

# Configura para mostrar todas as linhas do DataFrame
pd.set_option('display.max_rows', None)

# Lê arquivo CSV
df = pd.read_csv('operacao.csv', encoding='utf-8-sig', sep=';')

# Cria dicionário para mapear ticket → id do ativo
ticket_para_id = {ativo.ticket: ativo.pk for ativo in ativos}

# Cria coluna nova com o id do ativo baseado no ticket
df['id_ativo'] = df['ticket'].map(ticket_para_id).astype('Int64')

df = df.drop(columns=['ticket'])
df['classe'] = df['classe'].str.replace('A��o', 'Ação')
df['tipo_operacao'] = df['tipo_operacao'].str.replace('Bonifica��o ', 'Bonificação')
df = df[df['tipo_operacao'] != 'Venda']




print(df)


# for ticket, id_ in ticket_para_id.items():
#     print(f"Ticket: {ticket} → ID: {id_}")

