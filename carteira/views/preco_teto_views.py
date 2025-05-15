from decimal import Decimal
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from utils.cotacao import obter_cotacao
from carteira.forms import PrecoTetoForms
from carteira.models import PrecoTeto, Ativos
from utils.media_dividendos import media_dividendos
from django.contrib.messages.views import SuccessMessageMixin
from utils.debug_print import debu_print
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.core.cache import cache

#READ
class PrecoTetoRender(ListView):
    model = PrecoTeto
    template_name = 'preco_teto/list.html'
    context_object_name = 'lists'
    paginate_by = 10

    def get_queryset(self):
        filter_name = self.request.GET.get('name')
        queryset = PrecoTeto.objects.filter(fk_user_id=self.request.user.id,).order_by('id_ativo')  # Ordenando pela chave 'id_ativo'
        if filter_name:
            # Filtro aplicado diretamente no queryset
            queryset = queryset.filter(classe__icontains=filter_name)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ativos = self.get_queryset()  # Queryset já ordenado e filtrado, se necessário
        lista_ativos = {}
        tickers = [ativo.id_ativo for ativo in ativos]
        lista_ativos_acao = []
        lista_ativos_fii = []
        
        # Recupera os dados do cache que foi setado na funçao o obter_cotacao
        cotacoes = 0#obter_cotacao(tickers)
        
        # Busca médias de dividendos de uma só vez para evitar múltiplas chamadas
        # dividendos_cache = {ativo.id_ativo: media_dividendos(self.request.user.id,ativo.id_ativo, ativo.classe, 5) for ativo in ativos}
        dividendos_cache = {ativo.id_ativo: 10 for ativo in ativos}
        
        for ativo in ativos:
            cotacao = cotacoes.get(ativo.id_ativo) if cotacoes else None
           # Busca no dicionário dividendos_cache pelo valor associado à chave ativo.id_ativo.
            dividendos = dividendos_cache.get(ativo.id_ativo, Decimal(0))
            rentabilidade = Decimal(ativo.rentabilidade)  # Converte string para Decimal
            preco_teto_acoes = Decimal(dividendos)/(rentabilidade/100)
            ipca = Decimal(ativo.ipca) if ativo.ipca is not None else Decimal(0)
            preco_teto_fii = (Decimal(dividendos)/(ipca+ativo.rentabilidade))*100
            preco_teto = preco_teto_acoes if ativo.classe == "Ação" else preco_teto_fii
            diferenca = Decimal(cotacao or 0)-preco_teto
            margem_seguranca = ((preco_teto - Decimal(cotacao or 0))/preco_teto)*100
            recomendacao = "Comprar" if diferenca < 0 else "Não comprar"

            lista_ativos={
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
            }
            
            if ativo.classe == "Ação":
                lista_ativos_acao.append(lista_ativos)
            elif ativo.classe == "FII" or ativo.classe == "FII-Infra":
                lista_ativos_fii.append(lista_ativos)
                


        context['lista_ativos_acao'] = lista_ativos_acao
        context['lista_ativos_fii'] = lista_ativos_fii
        context['page_name'] = {'key':4,"page":"Preço Teto"}

        
        #context['lists'] = lista_ativos  # Adiciona a lista de ativos ao contexto
        
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
    

# def filtrar_ativos(request):
#     classe = request.GET.get('classe', '')
    
#     # Filtra os ativos com base na classe
#     ativos = Ativos.objects.filter(classe=classe,fk_user_id=request.user.id,)
    
#     # Prepara a resposta em formato JSON
#     ativos_data = [{'id': ativo.pk, 'nome': ativo.ticket} for ativo in ativos]
#     return JsonResponse({'ativos': ativos_data})
