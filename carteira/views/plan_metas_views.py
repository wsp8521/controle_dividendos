import json
from datetime import datetime
from django.db.models import Q, Sum 
from carteira.forms import PlanForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from utils.cotacao import obter_cotacao
from decimal import Decimal,InvalidOperation
from django.shortcuts import get_object_or_404, render
from utils.media_dividendos import media_dividendos
from carteira.models import PlanMetas, PrecoTeto, Ativos, MetaAtivo, Operacao, PlanMetasCalc
from django.views.generic import ListView, DeleteView, CreateView

class PlanMetasRender(ListView):
    model = PlanMetas
    template_name = 'plan_metas/list.html'
    context_object_name = 'lists'
    paginate_by = 10

    def get_queryset(self):
        filter = self.request.GET.get('classe')
        queryset = PlanMetas.objects.all().order_by('id_ativo')
        filter_ano = self.request.GET.get('ano')  # Captura o ano do filtro
        ano_atual = datetime.now().year

        if filter:
            queryset = queryset.filter(classe__icontains=filter)
            
        if filter_ano:
            queryset = queryset.filter(ano=filter_ano)  # Aplica o filtro de ano selecionado
        else:
             queryset = queryset.filter(ano=ano_atual)  # Aplica o filtro de ano atual       
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_metas = self.get_queryset()
        filter_status = self.request.GET.get('status')  # Pega o filtro de status da URL
        filter_ano = self.request.GET.get('ano') if self.request.GET.get('ano') else datetime.now().year
        filter_classe = self.request.GET.get('classe')  # Captura a classe do filtro no template
        filter_recomendacao = self.request.GET.get('recomendacao')  # Filtro para recomendação
        anos_lista = PlanMetas.objects.values_list('ano', flat=True).distinct().order_by('-ano')
        filter_ativo = Q(ano=filter_ano) if filter_classe is None else Q(ano=filter_ano) & Q(classe=filter_classe)
        
        #exibindo quantiadde total de ativos com base no ano e na calsse
        meta_geral = MetaAtivo.objects.filter(filter_ativo).aggregate(Sum("meta_geral"))['meta_geral__sum']  
        meta_anual = MetaAtivo.objects.filter(filter_ativo).aggregate(Sum("meta_anual"))['meta_anual__sum']  
        
        lista_ativos = []
       
        for plan in plan_metas:
            get_preco_teto = PrecoTeto.objects.filter(id_ativo=plan.id_ativo).first()
            ativos = Ativos.objects.filter(ticket=plan.id_ativo).first()
            cota_restante = plan.qtd - ativos.qtdAtivo if (plan.qtd - ativos.qtdAtivo) > 0 else 0
            cotacao = obter_cotacao(plan.id_ativo)
            dividendos = media_dividendos(plan.id_ativo, plan.classe, 5)
            rentabilidade = Decimal(get_preco_teto.rentabilidade)
            preco_teto_acoes = Decimal(dividendos) / (rentabilidade / 100)
            ipca = Decimal(get_preco_teto.ipca) if get_preco_teto.ipca is not None else Decimal(0)
            preco_teto_fii = (Decimal(dividendos) / (ipca + get_preco_teto.rentabilidade)) * 100
            preco_teto = preco_teto_acoes if plan.classe == "Ação" else preco_teto_fii
            cotacao_limpo = cotacao.replace("R$", "").strip().replace(",", ".")
            diferenca = Decimal(cotacao_limpo) - preco_teto
            total = Decimal(cotacao_limpo) * cota_restante if cota_restante > 0 else 0
            recomendacao = "Comprar" if diferenca < 0 else "Não comprar"
            
            if plan.qtd == ativos.qtdAtivo:
                status_meta = "Alcançada"
            elif ativos.qtdAtivo > plan.qtd:
                status_meta = "Ultrapassada"
            else:
                status_meta = "Não alcançada"
                    
            lista_ativos.append({
                "pk": plan.id,
                "ativo": plan.id_ativo,
                "qtd": plan.qtd,
                "classe": plan.classe,
                "cota_restante": cota_restante,
                "qtd_atual": ativos.qtdAtivo,
                "rentabilidade": rentabilidade,
                "cotacao": cotacao,
                "preco_teto": preco_teto,
                "diferenca": diferenca,
                "recomendacao": recomendacao,
                "status": status_meta,
                "total": total,
                "ano": plan.ano
            })
        
        # Aplicando o filtro de status
        if filter_status:
            lista_ativos = [item for item in lista_ativos if item["status"] == filter_status]
                
        if filter_recomendacao:
            lista_ativos = [item for item in lista_ativos if item["recomendacao"] == filter_recomendacao]
            
        #obtendo total necessário apra investimento
        invesimento_total = sum(item["total"] for item in lista_ativos)

        # Ordena os anos em ordem decrescente
        anos_unicos = sorted(set(anos_lista), reverse=True)
        meta_alcancada = Operacao.objects.filter(filter_ativo & ~Q(tipo_operacao="Venda")).aggregate(Sum("qtd"))['qtd__sum'] or 0
        meta_status = f"Falta {meta_anual-meta_alcancada}" if meta_anual-meta_alcancada>=0 else f'Superado {(meta_anual-meta_alcancada)*-1}'
        
        # context['total_ativo'] = PlanMetas.objects.aaggregate
        context['ano_atual'] = datetime.now().year
        context['investimento_total'] = invesimento_total
        context['meta_geral'] = meta_geral
        context['meta_anual'] = meta_anual
        context['meta_alcancada'] = meta_alcancada
        context['meta_status'] = meta_status
        context['lists'] = lista_ativos
        context['anos_disponiveis'] = anos_unicos  # Passando anos agrupados para o template
        return context


# #CRETE
class CadastroPlan(CreateView):
    model = PlanMetas
    form_class = PlanForm
    template_name = 'plan_metas/forms.html'
    success_url = reverse_lazy('list_plan')
    success_message = 'Cadastro realizado com sucesso'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.fk_user = self.request.user  # Define o usuário autenticado
        object.ano = datetime.now().year         
        object.save()
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 
    
#UPDATE
def atualizar_metas(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Obtém os dados passados no JavaScript
            meta = get_object_or_404(PlanMetas, id=pk)  # Obtém o objeto PlanMetas

            # Tenta obter o objeto PlanMetasCalc, se não existir, apenas ignora
            try:
                investimento = PlanMetasCalc.objects.get(id=pk)
            except PlanMetasCalc.DoesNotExist:
                investimento = None

            # Atualiza os dados da PlanMetas
            if "qtd" in data:
                meta.qtd = int(data["qtd"])
            if "qtd_calc" in data:
                meta.qtd_calc = int(data["qtd_calc"])

            if "proventos" in data:
                try:
                    proventos = data["proventos"].strip().replace(",", ".")
                    meta.prov_cota = Decimal(proventos)
                except (InvalidOperation, ValueError):
                    return JsonResponse({"status": "error", "message": "Valor inválido para proventos"}, status=400)

            # Atualiza os dados do PlanMetasCalc se ele existir
            if investimento:
                if "valor_investimento" in data:
                    try:
                        investimento.valor_investido = Decimal(data["valor_investimento"].strip().replace(",", "."))
                        investimento.save()
                    except (InvalidOperation, ValueError):
                        return JsonResponse({"status": "error", "message": "Valor inválido para valor de investimento"}, status=400)

            # Salva as alterações na PlanMetas
            meta.save()

            return JsonResponse({"status": "success", "message": "Metas e investimento atualizados com sucesso!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Método inválido!"}, status=400)

# #DELET
class PlanDelete(DeleteView):
    model=PlanMetas
    success_url = reverse_lazy('list_plan')
    success_message='Cadastro excluído com sucesso.'
    

def filtrar_ativos(request):
    classe = request.GET.get('classe', '')
    
    # Filtra os ativos com base na classe
    ativos = Ativos.objects.filter(classe=classe)
    #ativos = Ativos.objects.filter(classe=classe, qtdAtivo__gt=0)
    
    # Prepara a resposta em formato JSON
    ativos_data = [{'id': ativo.pk, 'nome': ativo.ticket} for ativo in ativos]
    return JsonResponse({'ativos': ativos_data})

def calculadora_ativos(request):
    classe = request.GET.get('tipo_calc', '')
    queryset = PlanMetas.objects.filter(classe=classe).order_by('id_ativo')
    valor_investimento = PlanMetasCalc.objects.filter(classe=classe).first() 
  
    lista_ativos = []
    context = {}
       
    for plan in queryset:
        cotacao = obter_cotacao(plan.id_ativo)
        cotacao_limpo = cotacao.replace("R$", "").strip().replace(",", ".")
        total = plan.qtd_calc*Decimal(cotacao_limpo)
        total_provento =  plan.qtd_calc * Decimal(plan.prov_cota)
        soma_total_ativo  = queryset.aggregate(Sum('qtd_calc'))['qtd_calc__sum']
        soma_prov  = queryset.aggregate(Sum('prov_cota'))['prov_cota__sum']
        
        lista_ativos.append({
            "pk": plan.id,
            "ativo": plan.id_ativo,
            "cotacao":cotacao,
            "qtd_calc": plan.qtd_calc,
            "proventos":plan.prov_cota,
            'total': total,
            'total_provento':total_provento
            
        
        })
      
    #TOTAIS
    soma_total_diheiro = sum(ativo['total'] for ativo in lista_ativos)  
    soma_total_prov = sum(ativo['total_provento'] for ativo in lista_ativos) 
    
    print("xxxxxxxxxxxxxxxxxxxxx") 
    print(valor_investimento.id)
    
    context['ativos'] = lista_ativos  # Passa a lista correta para o template
    context['ativos'] = lista_ativos  # Passa a lista correta para o template
    context['soma_prov'] = soma_prov 
    context['soma_total_prov'] = soma_total_prov
    context['soma_total_diheiro'] = soma_total_diheiro
    context['soma_total_ativo'] = soma_total_ativo
    context["valor_investimento"] = valor_investimento.valor_investido
    context["id_class"] = valor_investimento.id
    
    context["saldo"] = valor_investimento.valor_investido - soma_total_diheiro
    
    return render(request, "plan_metas/calculadora.html", context)
    