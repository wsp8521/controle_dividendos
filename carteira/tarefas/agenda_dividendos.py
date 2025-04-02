from decimal import Decimal
from carteira.models import Proventos, Ativos
from utils.pgto_dividendos import busca_agenda_pagamento, filtrar_por_mes_ano


def agenda_dividendos(id_user):
    ativos = Ativos.objects.filter(fk_user_id = id_user, qtdAtivo__gt=0) #obtendo os ativos do usuáiro
    
    dados_proventos=[]
    registros_cadastrados = 0  # Contador de registros cadastrados
    
    for ativo in ativos:
        busca_proventos = busca_agenda_pagamento(ativo=ativo.ticket, classe=ativo.classe)
        proventos_filtrados = filtrar_por_mes_ano(busca_proventos) #filtra os proventos que serão pagos
    
        #dados_filtrados['classe'] = ativo.classe 
        
        # Adiciona novos indice á lista
        for item in proventos_filtrados:
            item["classe"] = ativo.classe
            item['qtdAtivo'] = ativo.qtdAtivo
            dados_proventos.append(item)
                
    for dados in dados_proventos:
        
        # #TRATAMETNO DOS DADOS
        
        # #obtendo a instancia da tabela Ativo
        ativo_instancia = ativos.filter(ticket=dados['ativo']).first()
        
        # #tratamento valor do proventos
        valor = dados['valor']
        valor_recebido = Decimal(valor.replace(",", ".")).quantize(Decimal("0.01"))  # Troca ',' por '.' se necessário
        
        # #tratamento data pagamento
        data_pagamento = dados['pagamento']
        data_pagamento = data_pagamento.date()  # Obtém apenas a data (sem horário)
        
        #Tratamento tipo pagamento
        if any(tipo in dados['tipo'] for tipo in ['Rendimento']):
            tipo_rendimento = "Dividendos"
        else:
            tipo_rendimento = dados['tipo']
        
        # Verifica se já existe um provento para evitar duplicação
        if not Proventos.objects.filter(
        fk_user_id=id_user,
        id_ativo=ativo_instancia,
        data_pgto=data_pagamento,
        valor_recebido=valor_recebido * dados['qtdAtivo'],
        ).exists():
        # Cadastrando os proventos
            Proventos.objects.create(
                fk_user_id=id_user,
                id_ativo=ativo_instancia,
                classe=dados['classe'],
                tipo_provento=tipo_rendimento,
                valor_recebido=valor_recebido * dados['qtdAtivo'],
                data_pgto=data_pagamento,
                ano=data_pagamento.year,
                mes=data_pagamento.strftime("%B")
            )
            registros_cadastrados += 1  # Incrementa contador

       # Retorna mensagem com o número de registros cadastrados ou informa que não houve cadastro
    if registros_cadastrados > 0:
        return f"✅ {registros_cadastrados} registro(s) cadastrado(s) com sucesso! ✅"
    else:
        return "⚠️ Nenhum registro foi cadastrado. ⚠️"