from datetime import datetime
from django.core.cache import cache
from django.urls import reverse_lazy
from django.http import JsonResponse
from carteira.forms import ProventosForm
from carteira.models import Proventos, Ativos
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView


#READ
class ProventosRender(ListView):
    model = Proventos
    template_name = 'proventos/list.html'
    context_object_name = 'lists'
    ordering = 'data_pgto'
    paginate_by = 20

    def get_queryset(self):
        queryset = cache.get('dividendos_listagem')  #recuperando dados no cache
               
        if not queryset:  # verificando se ha dados no chace. se nao tiver, buscar no banco de daos
            # Filtra as operações pelo usuário logado
            queryset = Proventos.objects.filter(fk_user_id=self.request.user.id,valor_recebido__gt=0).order_by(self.ordering)
            cache.set('dividendos_listagem', queryset, timeout=300)  # salva dados no cache
        
        # Aplica o filtro adicional caso tenha sido fornecido um nome (parâmetro GET)
        filter_name = self.request.GET.get('ativo')
        if filter_name:
            queryset = queryset.filter(id_ativo__ticket__icontains=filter_name)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proventos = self.get_queryset()

        # Cria uma lista com os dados para exibir na tabela
        dados_tabela = []
        for provento in proventos:
            try:
                # Busca o ativo relacionado ao provento pelo ticket
                ativo = Ativos.objects.get(ticket=provento.id_ativo, fk_user_id=self.request.user.id)
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
                'status': provento.status,
            })

        context['lists'] = dados_tabela
        return context
    
 
# #CRETE
class CadastroProventos(SuccessMessageMixin, CreateView):
    model = Proventos
    form_class = ProventosForm
    template_name = 'proventos/forms.html'
    success_url = reverse_lazy('list_proventos')
    success_message = 'Cadastro realizado com sucesso'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.fk_user = self.request.user  # Define o usuário autenticado
        
        # Captura o mês e o ano atuais
        object.mes = datetime.now().month
        object.ano = datetime.now().year
        object.save()
        cache.delete('dividendos_listagem')  # Limpa o cache
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 
    
#UPDATE
class ProventosUpdate(SuccessMessageMixin, UpdateView):
    model = Proventos
    template_name ='proventos/forms.html'
    form_class = ProventosForm
    success_url = reverse_lazy('list_proventos')
    success_message ='Atualizada realizado com sucesso'
    
    
    def form_valid(self, form):
        object = form.save(commit=False)
        cache.delete('dividendos_listagem')  # Limpa o cache
        object.save()
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url)
    

#DELETE
class ProventosDelete( SuccessMessageMixin, DeleteView):
    model=Proventos
    success_url = reverse_lazy('list_proventos')
    success_message='Cadastro excluído com sucesso.'
    
def filtrar_ativos(request):
    #classe = request.GET.get('classe', '')
    classe = "Ação"
    
    # Filtra os ativos com base na classe
    ativos = Ativos.objects.filter(classe=classe, qtdAtivo__gt=0, fk_user_id=request.user.id)
    
    # Prepara a resposta em formato JSON
    ativos_data = [{'id': ativo.pk, 'nome': ativo.ticket} for ativo in ativos]
    return JsonResponse({'ativos': ativos_data})
