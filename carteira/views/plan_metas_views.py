import json
from decimal import Decimal
from carteira.models import PlanMetas, PrecoTeto
from django.http import JsonResponse
from django.views.generic import ListView, UpdateView
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.cotacao import obter_cotacao
from utils.media_dividendos import media_dividendos
from django.urls import reverse_lazy

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
        ativos = self.get_queryset()
       
        lista_ativos = []
        
        for ativo in ativos:
            preco_teto = PrecoTeto.objects.filter(id_ativo=ativo.id_ativo).first()
            cotacao = obter_cotacao(ativo.id_ativo)
            dividendos = media_dividendos(ativo.id_ativo, ativo.classe, 5)
            #rentabilidade = Decimal(ativo.rentabilidade)
            #preco_teto_acoes = Decimal(dividendos) / (rentabilidade / 100)
            #ipca = Decimal(ativo.ipca) if ativo.ipca is not None else Decimal(0)
            ##preco_teto_fii = (Decimal(dividendos) / (ipca + ativo.rentabilidade)) * 100
            #preco_teto = preco_teto_acoes if ativo.classe == "AÇÃO" else preco_teto_fii
            #cotacao_limpo = cotacao.replace("R$", "").strip().replace(",", ".")
            ##diferenca = Decimal(cotacao_limpo) - preco_teto
            #margem_seguranca = ((preco_teto - Decimal(cotacao_limpo)) / preco_teto) * 100
            #recomendacao = "Comprar" if diferenca < 0 else "Não comprar"
            
            
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print(preco_teto.rentabilidade)
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

            lista_ativos.append({
                "pk": ativo.id,
                "ativo": ativo.id_ativo,
                "qtd": ativo.qtd,  # Adicionando a quantidade para edição
                #"classe": ativo.classe,
                "rentabilidade": preco_teto.rentabilidade,
                #"ipca": ativo.ipca if ativo.ipca is not None else 0,
                "cotacao": cotacao,
                # "preco_teto": preco_teto,
                # "diferenca": diferenca,
                # "margem_seguranca": margem_seguranca if margem_seguranca >= 1 else 0,
                # "recomendacao": recomendacao,
            })
        context['lists'] = lista_ativos
        return context


# #CRETE
# class CadastroPrecoTeto(SuccessMessageMixin, CreateView):
#     model = PrecoTeto
#     form_class = PrecoTetoForms
#     template_name = 'preco_teto/forms.html'
#     success_url = reverse_lazy('list_preco_teto')
#     success_message = 'Cadastro realizado com sucesso'

#     def form_valid(self, form):
#         object = form.save(commit=False)
#         object.fk_user = self.request.user  # Define o usuário autenticado
#         object.save()
#         return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 
    
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
# class PrecoTetoDelete(SuccessMessageMixin, DeleteView):
#     model=PrecoTeto
#     success_url = reverse_lazy('list_preco_teto')
#     success_message='Cadastro excluído com sucesso.'
    

# def filtrar_ativos(request):
#     classe = request.GET.get('classe', '')
    
#     # Filtra os ativos com base na classe
#     ativos = Ativos.objects.filter(classe=classe)
    
#     # Prepara a resposta em formato JSON
#     ativos_data = [{'id': ativo.pk, 'nome': ativo.ticket} for ativo in ativos]
#     return JsonResponse({'ativos': ativos_data})
