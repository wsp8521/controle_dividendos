import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from carteira.models import Ativos, SetorAtivo, Corretora  # Substitua 'ativos_app' pelo nome real do seu app

class Command(BaseCommand):
    help = 'Importa ativos a partir de um arquivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('caminho_csv', type=str, help='Caminho para o arquivo CSV a ser importado')

    def handle(self, *args, **kwargs):
        caminho_csv = kwargs['caminho_csv']

        try:
            df = pd.read_csv(caminho_csv, encoding='latin1', sep=';')
        except Exception as e:
            self.stderr.write(f"Erro ao ler o CSV: {e}")
            return

        df.columns = df.columns.str.strip()

        def parse_moeda(valor):
            try:
                return float(str(valor).replace("R$", "").replace(".", "").replace(",", ".").strip())
            except:
                return None

        user = User.objects.first()
        if not user:
            self.stderr.write("Nenhum usuário encontrado no banco de dados.")
            return

        criados = 0
        for _, row in df.iterrows():
            try:
                ativo_nome = str(row['ativo']).strip()
                ticket = str(row['ticket']).strip()
                classe = str(row['classe']).strip()  # fixo, mas pode ser adaptado se vier no CSV
                cnpj = str(row['cnpj']).strip()

                # SetorAtivo
                setor_nome = str(row['setor']).strip()
                setor_obj, _ = SetorAtivo.objects.get_or_create(
                    setor=setor_nome,
                    defaults={'fk_user': user, 'setor_classe': None}
                )

                # Corretora
                corretora_nome = str(row['corretora']).strip()
                corretora_obj, _ = Corretora.objects.get_or_create(
                    apelido=corretora_nome,
                    defaults={
                        'fk_user': user,
                        'nome_corretora': corretora_nome,
                        'cnpj': ''
                    }
                )

                qtd = int(row['qtdAtivo']) if pd.notna(row['qtdAtivo']) else None
                investimento = parse_moeda(row['investimento'])
                dividendos = parse_moeda(row['dividendos'])

                Ativos.objects.create(
                    fk_user=user,
                    ativo=ativo_nome,
                    ticket=ticket,
                    classe=classe,
                    cnpj=cnpj,
                    setor=setor_obj,
                    corretora=corretora_obj,
                    qtdAtivo=qtd,
                    investimento=investimento,
                    dividendos=dividendos
                )
                criados += 1
            except Exception as e:
                self.stderr.write(f"Erro na linha: {row.to_dict()} - {e}")
        
        self.stdout.write(self.style.SUCCESS(f"{criados} ativos importados com sucesso."))
