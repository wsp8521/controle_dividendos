from carteira.models import Proventos, Ativos
from utils.pgto_dividendos import busca_agenda_pagamento
from datetime import datetime
from decimal import Decimal


def agenda_dividendos(request):
    dados_filtrados = []  # Lista para armazenar apenas os ativos com data de pagamento válida

    if request.user.is_authenticated:
        # Filtrar os ativos do usuário logado
        ativos = Ativos.objects.filter(fk_user=request.user.id)
        dados={}

        for ativo in ativos:
            dados = busca_agenda_pagamento(ativo=ativo.ticket, classe=ativo.classe)
            
                # Adiciona a classe do ativo ao dicionário de dados
            dados["classe"] = ativo.classe
            
            #filtrando apenas os ativos que possuem data de pagamento divulgado
            if dados["pagamento"] != "-":
                dados_filtrados.append(dados)
            
        # Exibir os dados filtrados
        for dados in dados_filtrados:
        
            # #tratamento valor do proventos
            valor = dados.get('valor')
            valor_recebido = Decimal(valor.replace(",", ".")).quantize(Decimal("0.01"))  # Troca ',' por '.' se necessário
            
            #tratamento data pagamento
            data_pagamento = dados.get('pagamento')
            data_pagamento = datetime.strptime(data_pagamento, "%d/%m/%Y").date()
            
            # Buscar a instância correta do ativo baseado no ticket e no usuário logado
            ativo_instancia = ativos.get(ticket=dados['ativo'])
            print(f"ATIVO {dados['ativo']} -  classe {dados['classe']}")

            # Verifica se já existe um provento para evitar duplicação
            if not Proventos.objects.filter(
                fk_user=request.user,
                id_ativo=ativo_instancia,
                data_pgto=data_pagamento,
                valor_recebido=valor_recebido
            ).exists():
                # Cadastrando os proventos
                Proventos.objects.create(
                    fk_user=request.user,
                    id_ativo=ativo_instancia,
                    classe=dados['classe'],
                    tipo_provento=dados['tipo'],
                    valor_recebido=valor_recebido,
                    data_pgto=data_pagamento,
                    ano=data_pagamento.year,
                    mes=data_pagamento.strftime("%B")
                )
