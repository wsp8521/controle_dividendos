from decimal import Decimal
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from utils.cotacao import obter_cotacao
from carteira.forms import PrecoTetoForms
from carteira.models import PrecoTeto, Ativos
from utils.media_dividendos import media_dividendos
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from utils.debug_print import debu_print

#READ
class PrecoTetoRender(ListView):
    model = PrecoTeto
    template_name = 'preco_teto/list.html'
    context_object_name = 'lists'
    paginate_by = 10

    def get_queryset(self):
        filter_name = self.request.GET.get('name')
        queryset = PrecoTeto.objects.all().order_by('id_ativo')  # Ordenando pela chave 'id_ativo'
        if filter_name:
            # Filtro aplicado diretamente no queryset
            queryset = queryset.filter(classe__icontains=filter_name)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ativos = self.get_queryset()  # Queryset já ordenado e filtrado, se necessário
        lista_ativos = []
        
        for ativo in ativos:
            cotacao = obter_cotacao(ativo.id_ativo)
            dividendos = media_dividendos(ativo.id_ativo, ativo.classe, 5)
            rentabilidade = Decimal(ativo.rentabilidade)  # Converte string para Decimal
            preco_teto_acoes = Decimal(dividendos)/(rentabilidade/100)
            ipca = Decimal(ativo.ipca) if ativo.ipca is not None else Decimal(0)
            preco_teto_fii = (Decimal(dividendos)/(ipca+ativo.rentabilidade))*100
            preco_teto = preco_teto_acoes if ativo.classe == "AÇÃO" else preco_teto_fii
            cotacao_limpo = cotacao.replace("R$", "").strip().replace(",", ".")  # Remove "R$" e troca vírgula por ponto
            diferenca = Decimal(cotacao_limpo)-preco_teto
            margem_seguranca = ((preco_teto - Decimal(cotacao_limpo))/preco_teto)*100
            recomendacao = "Comprar" if diferenca < 0 else "Não comprar"

            lista_ativos.append({
                "pk": ativo.id,  # Chave primária
                "ativo": ativo.id_ativo,
                "classe": ativo.classe,
                "rentabilidade": ativo.rentabilidade,
                "ipca": ativo.ipca if ativo.ipca is not None else 0,
                "cotacao": cotacao,
                "preco_teto": preco_teto,
                "diferenca": diferenca,
                "margem_seguranca": margem_seguranca if margem_seguranca >= 1 else 0,
                "recomendacao": recomendacao,
            })

        context['lists'] = lista_ativos  # Passando a lista dos ativos para o contexto
        return context

#CRETE
class CadastroPrecoTeto(SuccessMessageMixin, CreateView):
    model = PrecoTeto
    form_class = PrecoTetoForms
    template_name = 'preco_teto/forms.html'
    success_url = reverse_lazy('list_preco_teto')
    success_message = 'Cadastro realizado com sucesso'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.fk_user = self.request.user  # Define o usuário autenticado
        object.save()
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 
    
#UPDATE
class PrecoTetoUpdate(SuccessMessageMixin, UpdateView):
    model = PrecoTeto
    template_name ='preco_teto/form_edit.html'
    form_class = PrecoTetoForms
    success_url = reverse_lazy('list_preco_teto')
    success_message ='Atualizada realizado com sucesso'
    
  
#DELETE
class PrecoTetoDelete(SuccessMessageMixin, DeleteView):
    model=PrecoTeto
    success_url = reverse_lazy('list_preco_teto')
    success_message='Cadastro excluído com sucesso.'
    

def filtrar_ativos(request):
    classe = request.GET.get('classe', '')
    
    # Filtra os ativos com base na classe
    ativos = Ativos.objects.filter(classe=classe)
    
    # Prepara a resposta em formato JSON
    ativos_data = [{'id': ativo.pk, 'nome': ativo.ticket} for ativo in ativos]
    return JsonResponse({'ativos': ativos_data})
