
import json
import datetime
from django.db.models import Sum 
from django.core.cache import cache
from utils.cotacao import obter_cotacao
from decimal import Decimal
from django.shortcuts import render
from carteira.models import PlanMetas, PlanMetasCalc
from babel.numbers import format_currency
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from decimal import Decimal,InvalidOperation
from django.contrib import messages


def calculadora_ativos(request):
    classe = request.GET.get('tipo_calc', '')
    queryset = PlanMetas.objects.filter(
        classe__icontains=classe, 
        fk_user_id=request.user.id,
        ano = datetime.datetime.now().year,
        ).order_by('id_ativo')
    valor_investimento = PlanMetasCalc.objects.filter(classe__icontains=classe, fk_user_id=request.user.id).first()
    
    context = {}
    lista_ativos = []
    tickers = [ativo.id_ativo for ativo in queryset]

    # Recupera cotações do cache ou consulta
    cache_key = "cotacao_key"
    cotacoes = cache.get(cache_key)
    if not cotacoes:
        cotacoes = obter_cotacao(tickers)

    # Calcula agregados, mesmo se queryset estiver vazio
    soma_total_ativo = queryset.aggregate(Sum('qtd_calc'))['qtd_calc__sum'] or 0
    soma_prov = queryset.aggregate(Sum('prov_cota'))['prov_cota__sum'] or 0

    for plan in queryset:
        cotacao = cotacoes.get(f'{plan.id_ativo}.SA') if cotacoes else None
        total = plan.qtd_calc * Decimal(cotacao or 0)
        total_provento = plan.qtd_calc * Decimal(plan.prov_cota)

        lista_ativos.append({
            "pk": plan.id,
            "ativo": plan.id_ativo,
            "cotacao": cotacao,
            "qtd_calc": plan.qtd_calc,
            "proventos": plan.prov_cota,
            'total': format_currency(total, "BRL", locale="pt_BR"),
            'total_soma': total,
            'total_provento': total_provento
        })

    soma_total_diheiro = sum(ativo['total_soma'] for ativo in lista_ativos)
    soma_total_prov = sum(ativo['total_provento'] for ativo in lista_ativos)

    # Trata valor_investimento = None
    if valor_investimento:
        valor_investido = valor_investimento.valor_investido
        saldo = valor_investido - soma_total_diheiro
        context["valor_investimento"] = valor_investido
        context["id_class"] = valor_investimento.id
        context["saldo"] = format_currency(saldo, "BRL", locale="pt_BR")
    else:
        messages.warning(request, "Você ainda não cadastrou o valor investido para essa classe.")
        context["valor_investimento"] = Decimal(0)
        context["id_class"] = None
        context["saldo"] = format_currency(0, "BRL", locale="pt_BR")

    # Preenche o restante do contexto
    context['ativos'] = lista_ativos
    context['soma_prov'] = format_currency(soma_prov, "BRL", locale="pt_BR")
    context['soma_total_prov'] = format_currency(soma_total_prov, "BRL", locale="pt_BR")
    context['soma_total_diheiro'] = format_currency(soma_total_diheiro, "BRL", locale="pt_BR")
    context['soma_total_ativo'] = soma_total_ativo
    context['is_ativo'] = True if queryset.exists() else False

    return render(request, "plan_metas/partials/calculadora.html", context)

#alterar a quantidade de ativos 
def update_valor_investido(request, pk):
    if request.method == "POST":
        try:
            # Tenta carregar os dados JSON do corpo da requisição
            data = json.loads(request.body)

            # Obtém o objeto PlanMetasCalc com o pk fornecido, filtrando para o usuário logado
            investimento = get_object_or_404(PlanMetasCalc, id=pk, fk_user=request.user)
            

            # Verifique se o campo valor_investido está no corpo da requisição
            if "valor_investimento" in data:
                # Atualiza o valor investido
                valor_investido = int(data["valor_investimento"])
                investimento.valor_investido = valor_investido

            # Salva o objeto PlanMetasCalc atualizado
            investimento.save()

            # Retorna resposta de sucesso
            return JsonResponse({"status": "success"})

        except Exception as e:
            # Retorna erro com a mensagem da exceção
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    # Retorna erro caso o método não seja POST
    return JsonResponse({"status": "error", "message": "Método inválido!"}, status=400)

#Criar regisgtro
def create_valor_investido(request):
    if request.method == "POST":
        try:
            # Tenta carregar os dados JSON do corpo da requisição
            data = json.loads(request.body)
            registro_existente = PlanMetasCalc.objects.filter(fk_user=request.user, classe=data.get("tipo_calc", "")).first()
           
            # Verifique se o campo valor_investimento está no corpo da requisição
            if "valor_investimento" in data:
                valor_investido = int(data["valor_investimento"])
                
                
                if registro_existente:
                       return JsonResponse({"status": "error", "message": "Já existe um registro para esse tipo de ativo."}, status=400)

                # Cria um novo registro de PlanMetasCalc associado ao usuário logado
                investimento = PlanMetasCalc(
                    fk_user=request.user,  # Associa o registro ao usuário logado
                    classe=data.get("tipo_calc", ""),  # Classe pode ser opcional, dependendo do envio
                    valor_investido=valor_investido,
                    
                )

                # Salva o novo registro no banco de dados
                investimento.save()

                # Retorna resposta de sucesso
                return JsonResponse({"status": "success", "message": "Registro criado com sucesso!"})

            # Caso o campo 'valor_investimento' não seja fornecido
            return JsonResponse({"status": "error", "message": "Campo 'valor_investimento' não encontrado."}, status=400)

        except Exception as e:
            # Retorna erro com a mensagem da exceção
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    # Retorna erro caso o método não seja POST
    return JsonResponse({"status": "error", "message": "Método inválido!"}, status=400)