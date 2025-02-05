import json
from decimal import Decimal
from carteira.forms import PlanForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from utils.cotacao import obter_cotacao
from django.shortcuts import get_object_or_404
from utils.media_dividendos import media_dividendos
from carteira.models import PlanMetas, PrecoTeto, Ativos
from django.views.generic import ListView, DeleteView, CreateView

class PlanMetasRender(ListView):
    model = PlanMetas
    template_name = 'plan_metas/list.html'
    context_object_name = 'lists'
    paginate_by = 10

    def get_queryset(self):
        filter_name = self.request.GET.get('name')
        queryset = PlanMetas.objects.all().order_by('id_ativo')
        if filter_name:
            queryset = queryset.filter(classe__icontains=filter_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_metas = self.get_queryset()
       
        lista_ativos = []
        
        for plan in plan_metas:
            get_preco_teto = PrecoTeto.objects.filter(id_ativo=plan.id_ativo).first()
            ativos = Ativos.objects.filter(ticket=plan.id_ativo).first()
            cota_restante = plan.qtd-ativos.qtdAtivo if (plan.qtd-ativos.qtdAtivo)> 0 else 0
            cotacao = obter_cotacao(plan.id_ativo)
            dividendos = media_dividendos(plan.id_ativo, plan.classe, 5)
            rentabilidade = Decimal(get_preco_teto.rentabilidade)
            preco_teto_acoes = Decimal(dividendos)/ (rentabilidade / 100)
            ipca = Decimal(get_preco_teto.ipca) if get_preco_teto.ipca is not None else Decimal(0)
            preco_teto_fii = (Decimal(dividendos) / (ipca + get_preco_teto.rentabilidade)) * 100
            preco_teto = preco_teto_acoes if plan.classe == "Ação" else preco_teto_fii
            cotacao_limpo = cotacao.replace("R$", "").strip().replace(",", ".")
            diferenca = Decimal(cotacao_limpo) - preco_teto
            total = Decimal(cotacao_limpo) * cota_restante if cota_restante >0 else 0
            recomendacao = "Comprar" if diferenca < 0 else "Não comprar"
            
            if plan.qtd == ativos.qtdAtivo:
                status_meta = "alcançada"
            elif ativos.qtdAtivo > plan.qtd:
                status_meta = "ultrapassada"
            else:
                status_meta = "não alcançada"
                 
            lista_ativos.append({
                "pk": plan.id,
                "ativo": plan.id_ativo,
                "qtd": plan.qtd,  # Adicionando a quantidade para edição
                "classe": plan.classe,
                "cota_restante": cota_restante,
                "qtd_atual":ativos.qtdAtivo,
                "rentabilidade": rentabilidade,
                "cotacao": cotacao,
                "preco_teto": preco_teto,
                "diferenca": diferenca,
                "recomendacao": recomendacao,
                "status": status_meta,
                "total":total
            })
        context['lists'] = lista_ativos
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
        object.save()
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 
    
#UPDATE
def atualizar_metas(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            novo_valor = data.get("novo_valor")

             # Busca o objeto pelo 'pk' recebido na URL
            meta = get_object_or_404(PlanMetas, id=pk)
            meta.qtd = int(novo_valor)
            meta.save()
            return JsonResponse({"status": "success", "message": "Meta atualizada com sucesso!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Método inválido!"}, status=400)


# #DELETE

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
