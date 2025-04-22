import locale
import json
from decimal import Decimal
from django.db.models import Sum, Q
from carteira.models import Ativos
from django.core.cache import cache
from django.urls import reverse_lazy
from django.http import JsonResponse
from carteira.forms import AtivosForm
from utils.cotacao import obter_cotacao
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from carteira.dados_graficos.metric_chart_detail_ativo import chart_ativo_proventos

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#READ
class AtivoRender(ListView):
    model = Ativos
    template_name = 'ativos/list.html'
    context_object_name = 'lists'
    ordering = '-qtdAtivo'
    paginate_by = 20

    def get_queryset(self):
        self.filter_url_pag_nav = ""#Criando um atributo da instância da classe, acessível por qualquer método da mesma view
        queryset = Ativos.objects.filter(fk_user_id=self.request.user.id).order_by(self.ordering)
        filter_name = self.request.GET.get('ativo')
        filter_classe = self.request.GET.get('classe_ativos') 
    
        if filter_name:
            return queryset.filter(
                Q(ativo__icontains=filter_name) |
                Q(ticket__icontains=filter_name) 
                #Q(setor__setor__icontains=filter_name)  # <- correção aqui
            ).order_by(self.ordering)
            
        if filter_classe:
            self.filter_url_pag_nav = filter_classe
            queryset = queryset.filter(classe=filter_classe)      
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Use o queryset paginado já fornecido pelo ListView
        page_obj = context['page_obj']  # já paginado
        ativos = page_obj.object_list
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
                "cotacao": locale.currency(cotacao, grouping=True) if cotacao else 0,
                "qtd": ativo.qtdAtivo if ativo.qtdAtivo is not None else 0,
                "investimento":  locale.currency(ativo.investimento, grouping=True) if ativo.investimento else 0,
                "dividendos":  locale.currency(ativo.dividendos, grouping=True) if ativo.dividendos else 0,
            })

        context['lists'] = lista_ativos
        filter_url = getattr(self, 'filter_url_pag_nav', None)   #url que será aplicado na paginação quado o usuário aplicar algum filtro
        context['url_filter_pagination'] = f'&classe_ativos={filter_url}' if filter_url else ""
        return context

#DETAIL
class AtivoDetail(DetailView):
    model = Ativos
    template_name = "ativos/detail.html"
    context_object_name = 'lists'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ativo = self.get_object()
        dados_graficos = chart_ativo_proventos(self.request.user.id, ativo)
        render_grafico = True
        
        # Preço médio de aquisição
        preco_medio = ativo.investimento / ativo.qtdAtivo if ativo.qtdAtivo and ativo.investimento else 0  

        # Obter cotação atual
        cotacoes = obter_cotacao([ativo.ticket])
        cotacao = cotacoes.get(f"{ativo.ticket}.SA")

        # Valor de mercado = cotação atual * quantidade de cotas
        valor_mercado = Decimal(cotacao) * ativo.qtdAtivo if cotacao and ativo.qtdAtivo else 0

        # Valorização = valor de mercado - investimento (lucro/prejuízo não realizado)
        lucro_ou_prejuizo = valor_mercado - ativo.investimento if ativo.investimento else 0

        # Rentabilidade líquida (exclui dividendos, pois são reinvestidos)
        rentabilidade = (lucro_ou_prejuizo / ativo.investimento * 100) if ativo.investimento else 0

        dados = {
            'ativo': ativo.ativo,
            'cotacao': locale.currency(cotacao, grouping=True) if cotacao else 0,
            'ticket': ativo.ticket,
            'classe': ativo.classe,
            'setor': ativo.setor,
            'cnpj': ativo.cnpj,
            'corretora': ativo.corretora,
            'qtdAtivo': ativo.qtdAtivo if ativo.qtdAtivo is not None else 0,
            'investimento': locale.currency(ativo.investimento, grouping=True) if ativo.investimento else 0,
            'proventos': locale.currency(ativo.dividendos, grouping=True) if ativo.dividendos else 0,  # apenas informativo
            'preco_medio': locale.currency(preco_medio, grouping=True),
            'valor_mercado': locale.currency(valor_mercado, grouping=True),
            'valorizacao': locale.currency(lucro_ou_prejuizo, grouping=True),
            'patrimonio': locale.currency(valor_mercado, grouping=True),  # patrimônio = valor de mercado atual
            'rentabilidade': round(rentabilidade, 2),
        }

        context['lists'] = dados
        context['grafico'] = {
            'grafico_operacao': json.dumps(dados_graficos['chart_operacao']),
            'grafico_proventos': json.dumps(dados_graficos['chart_proventos']),
        }
        context['render_grafico_detail_ativo'] = render_grafico

        return context

        
#CRETE
class CadastroAtivos(SuccessMessageMixin, CreateView):
    model = Ativos
    form_class = AtivosForm
    template_name = 'ativos/forms.html'
    success_url = reverse_lazy('list_ativo')
    success_message = 'Cadastro realizado com sucesso'
    
    #função par  inserir argumentos personalizados no formulário 
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Passa o usuário logado para o formulário
        return kwargs

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
        kwargs['user'] = self.request.user  # Passa o usuário logado para o formulário
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
    