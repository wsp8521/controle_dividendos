from datetime import datetime
from django.core.cache import cache
from django.urls import reverse_lazy
from django.http import JsonResponse
from carteira.forms import ProventosForm
from carteira.models import Proventos, Ativos
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView


#READ
class PagamentoRender(ListView):
    model = Proventos
    template_name = 'proventos/list.html'
    context_object_name = 'lists'
    ordering = '-data_pgto'
    paginate_by = 20

    def get_queryset(self):
        queryset = cache.get('operacao_listagem')  #recuperando dados no cache
               
        if not queryset:  # verificando se ha dados no chace. se nao tiver, buscar no banco de daos
            # Filtra as operações pelo usuário logado
            queryset = Proventos.objects.filter(fk_user=self.request.user).order_by(self.ordering)
            cache.set('produtos_listagem', queryset, timeout=300)  # salva dados no cache
        
        # Aplica o filtro adicional caso tenha sido fornecido um nome (parâmetro GET)
        filter_name = self.request.GET.get('name')
        if filter_name:
            queryset = queryset.filter(ticket__icontains=filter_name)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proventos = self.get_queryset()

        # Cria uma lista com os dados para exibir na tabela
        dados_tabela = []
        for provento in proventos:
            try:
                # Busca o ativo relacionado ao provento pelo ticket
                ativo = Ativos.objects.get(ticket=provento.id_ativo, fk_user=self.request.user)
                qtd_cota = ativo.qtdAtivo or 0  # Caso `qtdAtivo` seja nulo
            except Ativos.DoesNotExist:
                qtd_cota = 0

            valor_por_cota = float(provento.valor_recebido) / qtd_cota if qtd_cota > 0 else 0

            dados_tabela.append({
                "pk": provento.id,  # Chave primária
                'ativo': provento.id_ativo,
                'classe': provento.classe,
                'tipo': provento.tipo_provento,
                'valor': provento.valor_recebido,
                'qtd_cota': qtd_cota,
                'valor_por_cota': round(valor_por_cota, 2),
                'data_pgto': provento.data_pgto,
            })

        context['lists'] = dados_tabela
        return context
    
 
