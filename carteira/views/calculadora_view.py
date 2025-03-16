
import json
from django.db.models import Q, Sum 
from utils.cotacao import obter_cotacao
from decimal import Decimal
from django.shortcuts import render
from carteira.models import PlanMetas, PlanMetasCalc
from babel.numbers import format_currency
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from decimal import Decimal,InvalidOperation


def calculadora_ativos(request):
    classe = request.GET.get('tipo_calc', '')
    queryset = PlanMetas.objects.filter(classe__icontains=classe,fk_user_id=request.user.id,).order_by('id_ativo')
    valor_investimento = PlanMetasCalc.objects.filter(classe=classe,fk_user_id=request.user.id,).first() 
    lista_ativos = []
    context = {}
    tickers = [ativo.id_ativo for ativo in queryset]
    cotacoes = obter_cotacao(tickers)
       
    for plan in queryset:
        cotacao = cotacoes.get(f'{plan.id_ativo}.SA')
        total = plan.qtd_calc*Decimal(cotacao or 0)
        total_provento =  plan.qtd_calc * Decimal(plan.prov_cota)
        soma_total_ativo  = queryset.aggregate(Sum('qtd_calc'))['qtd_calc__sum']
        soma_prov  = queryset.aggregate(Sum('prov_cota'))['prov_cota__sum']
        
        lista_ativos.append({
            "pk": plan.id,
            "ativo": plan.id_ativo,
            "cotacao":cotacao,
            "qtd_calc": plan.qtd_calc,
            "proventos":plan.prov_cota,
            'total': format_currency(total, "BRL", locale="pt_BR"),
            'total_soma': total,
            'total_provento':total_provento
        
        })
      
    #TOTAIS
    soma_total_diheiro = sum(ativo['total_soma'] for ativo in lista_ativos)  
    soma_total_prov = sum(ativo['total_provento'] for ativo in lista_ativos) 
    context['ativos'] = lista_ativos  # Passa a lista correta para o template

    context['soma_prov'] = format_currency(soma_prov , "BRL", locale="pt_BR")
    context['soma_total_prov'] = format_currency(soma_total_prov, "BRL", locale="pt_BR")
    context['soma_total_diheiro'] = format_currency(soma_total_diheiro, "BRL", locale="pt_BR")
    context['soma_total_ativo'] = soma_total_ativo 
    context["valor_investimento"] = valor_investimento.valor_investido 
    context["id_class"] = valor_investimento.id
    
    saldo = valor_investimento.valor_investido - soma_total_diheiro
    context["saldo"] = format_currency(saldo, "BRL", locale="pt_BR")
    
    return render(request, "plan_metas/calculadora.html", context)


#alterar a quantidade de ativos 
def update_valor_investido(request, pk):
      
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Obtém os dados passados no JavaScript
            investimento = get_object_or_404(PlanMetasCalc, id=pk)  # Obtém o objeto PlanMetas
            
            # Atualiza os dados da PlanMetasCalc
            if "valor_investimento" in data:
                investimento.valor_investido = int(data["valor_investimento"])
            investimento.save()
            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Método inválido!"}, status=400)



    
   