import pandas as pd
import unicodedata
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from carteira.models import Ativos, Proventos

def normalize_colname(colname):
    nfkd = unicodedata.normalize('NFKD', colname)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().replace(" ", "_")

class Command(BaseCommand):
    help = 'Importa operações a partir de um arquivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('caminho_csv', type=str, help='Caminho para o arquivo CSV a ser importado')

    def handle(self, *args, **kwargs):
        caminho_csv = kwargs['caminho_csv']

        try:
            # Cria dicionário para mapear ticket → id do ativo
            ativos = Ativos.objects.all()
            ticket_para_id = {ativo.ticket.strip().upper(): ativo.pk for ativo in ativos}
            
            # Configura para mostrar todas as linhas do DataFrame
            pd.set_option('display.max_rows', None)
            df = pd.read_csv(caminho_csv, sep=';', encoding='utf-8-sig')
            df['classe'] = df['classe'].str.replace('A��o', 'Ação')

    
            # Normaliza ticket no DataFrame para garantir correspondência
            # df['ticket'] = df['ticket'].str.strip().str.upper()

            # Mapeia id do ativo no DataFrame
            df['id_ativo'] = df['ticket'].map(ticket_para_id).astype('Int64')

            # # Remove coluna ticket após mapeamento
            df = df.drop(columns=['ticket'])
            
            #self.stdout.write(self.style.SUCCESS(f"{df} operações importadas com sucesso."))

        except Exception as e:
            self.stderr.write(f"Erro ao ler o CSV: {e}")
            return

        # Normaliza os nomes das colunas
        df.columns = [normalize_colname(c) for c in df.columns]
        
        #self.stdout.write(self.style.SUCCESS(f"{df} Lista de operações."))

        def parse_moeda(valor):
            try:
                return float(str(valor).replace("R$", "").replace(".", "").replace(",", ".").strip())
            except:
                return None

        def parse_data(valor):
            try:
                return pd.to_datetime(valor, dayfirst=True).date()
            except:
                return None

        user = User.objects.first()
        if not user:
            self.stderr.write("Nenhum usuário encontrado no banco de dados.")
            return

        criados = 0
        for _, row in df.iterrows():
            try:
                codigo_ativo = row.get('id_ativo')

                # Verifica se código do ativo é válido e converte para int
                if pd.isna(codigo_ativo):
                    self.stderr.write(f"Código de ativo inválido na linha: {row.to_dict()}")
                    continue

                codigo_ativo_int = int(float(codigo_ativo))

                ativo_obj = Ativos.objects.filter(pk=codigo_ativo_int).first()
                if not ativo_obj:
                    self.stderr.write(f"Ativo com id '{codigo_ativo_int}' não encontrado. Linha ignorada.")
                    continue

                classe = str(row['classe']).strip() if pd.notna(row['classe']) else ""
                data_pgto = parse_data(row.get('data_pgto'))
                valor_recebido = parse_moeda(row.get('valor_recebido'))
                tipo_provento = str(row['tipo_provento']).strip() if pd.notna(row['tipo_provento']) else None
                status = str(row['status'])

                mes = str(row['mes']).strip() if pd.notna(row['mes']) else None
                ano = int(row['ano']) if pd.notna(row['ano']) else None

                Proventos.objects.create(
                    fk_user=user,
                    id_ativo=ativo_obj,
                    classe=classe,
                    status=status,
                    tipo_provento=tipo_provento,
                    valor_recebido=valor_recebido,
                    data_pgto=data_pgto,
                    mes=mes,
                    ano=ano,
                )
                criados += 1
            except Exception as e:
                self.stderr.write(f"Erro na linha: {row.to_dict()} - {e}")

        self.stdout.write(self.style.SUCCESS(f"{criados} operações importadas com sucesso."))
