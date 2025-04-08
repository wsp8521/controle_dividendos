import locale
from carteira.models import Ativos
from django.core.cache import cache
from django.urls import reverse_lazy
from django.http import JsonResponse
from carteira.forms import AtivosForm
from utils.cotacao import obter_cotacao
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from utils.cotacao import obter_cotacao
from decimal import Decimal

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')



#READ
class AtivoRender(ListView):
    model = Ativos
    template_name = 'ativos/list.html'
    context_object_name = 'lists'
    ordering = 'ativo'
    paginate_by = 10

    def get_queryset(self):
        # Filtra as operações pelo usuário logado
        queryset = Ativos.objects.filter(fk_user_id=self.request.user.id).order_by(self.ordering)
        filter_name = self.request.GET.get('name')
        if filter_name:
            return queryset.filter(ticket__icontains=filter_name)
        return queryset 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ativos = self.get_queryset()
        tickers = [ativo.ticket for ativo in ativos]
        
        
        # Recupera os dados do cache que foi setado na funçao o obter_cotacao
        cache_key = "cotacao_key"
        cotacoes = cache.get(cache_key)

        if not cotacoes:
            cotacoes = obter_cotacao(tickers)  # Busca novas cotações e armazena no cache
        
        lista_ativos = []
        for ativo in ativos:
            cotacao = cotacoes.get(f'{ativo.ticket}.SA') if cotacoes else None
            lista_ativos.append({
                "pk": ativo.id,
                "ativo": ativo.ativo,
                "setor": ativo.setor,
                "cnpj": ativo.cnpj,
                "ticket": ativo.ticket,
                "classe": ativo.classe,
                "cotacao": cotacao,
                "qtd": ativo.qtdAtivo if ativo.qtdAtivo is not None else 0,
                "investimento": ativo.investimento if ativo.investimento else 0,
                "dividendos": ativo.dividendos if ativo.dividendos else 0,
            })

        context['lists'] = lista_ativos
        return context

#DETAIL
class AtivoDetail(DetailView):
    model = Ativos
    template_name = "ativos/detail.html"
    context_object_name='lists'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ativo = self.get_object()
        preco_medio = ativo.investimento / ativo.qtdAtivo if ativo.qtdAtivo else 0  
        cotacoes = obter_cotacao([ativo.ticket])  # Corrigido: envia como lista
        cotacao = cotacoes.get(f"{ativo.ticket}.SA")  # Busca a cotação do ativo específico
        valor_mercado = Decimal(cotacao) * ativo.qtdAtivo if cotacao and ativo.qtdAtivo else 0
        valorizacao = valor_mercado - ativo.investimento if ativo.investimento else 0
        patrimonio =  valor_mercado + ativo.dividendos + ativo.investimento if ativo.investimento else 0
        rentabilidade = (valorizacao + ativo.dividendos) / ativo.investimento * 100 if ativo.investimento else 0
        
    
        
        dados={
            'ativo': ativo.ativo,
            'cotacao': locale.currency(cotacao, grouping=True) if cotacao else 0,
            'ticket': ativo.ticket,
            'classe': ativo.classe,
            'setor': ativo.setor,
            'cnpj': ativo.cnpj, 
            'qtdAtivo':ativo.qtdAtivo if ativo.qtdAtivo is not None else 0,
            'investimento': locale.currency(ativo.investimento, grouping=True) or 0,
            'proventos': locale.currency(ativo.dividendos, grouping=True) or 0,
            'preco_medio': locale.currency(preco_medio, grouping=True),
            'valor_mercado': locale.currency(valor_mercado, grouping=True),
            'valorizacao': locale.currency(valorizacao, grouping=True) ,
            'patrimonio': locale.currency(patrimonio, grouping=True),
            'rentabilidade': rentabilidade,
            
        }
        
        context['lists'] = dados
        return context
        
       
       
       
    
#CRETE
class CadastroAtivos(SuccessMessageMixin, CreateView):
    model = Ativos
    form_class = AtivosForm
    template_name = 'ativos/forms.html'
    success_url = reverse_lazy('list_ativo')
    success_message = 'Cadastro realizado com sucesso'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.fk_user = self.request.user  # Define o usuário autenticado
        object.save()
        cache.delete('ativo_listagem')  # Limpa o cache
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 
    
#UPDATE
class AtivosUpdate(SuccessMessageMixin, UpdateView):
    model = Ativos
    template_name ='ativos/forms.html'
    form_class = AtivosForm
    success_url = reverse_lazy('list_ativo')
    success_message ='Atualizada realizado com sucesso'
   
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_edit'] = True  # Passa o parâmetro is_edit=True para o formulário
        return kwargs
    
    
    def form_valid(self, form):
        object = form.save(commit=False)
        cache.delete('ativo_listagem')  # Limpa o cache
        object.save()
        cache.delete('dividendos_listagem')  # Limpa o cache da pagina dividendos
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url)
    
#DELETE
class AtivoDelete( SuccessMessageMixin, DeleteView):
    model=Ativos
    success_url = reverse_lazy('list_ativo')
    success_message='Cadastro excluído com sucesso.'
    
#FUNÇÕES GERAIS
def atualizar_cotacao(request):
    """Remove os dados do cache e busca novas cotações."""
    cache_key = "cotacao_key"
    
    # Obtém os ativos do usuário logado
    ativos = Ativos.objects.filter(fk_user_id=request.user.id)
    tickers = [ativo.ticket for ativo in ativos]

    # Força a atualização das cotações
    novas_cotacoes = obter_cotacao(tickers)
    cache.set(cache_key, novas_cotacoes, timeout=600)  # Armazena por 10 minutos
    return JsonResponse({"status": "success", "mensagem": "Cotações atualizadas com sucesso!"})
