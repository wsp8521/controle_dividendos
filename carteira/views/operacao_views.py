from datetime import datetime
from django.core.cache import cache
from django.urls import reverse_lazy
from django.http import JsonResponse
from carteira.forms import OperacaoForm
from carteira.models import Operacao, Ativos
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView


#READ
class OperacaoRender(ListView):
    model = Operacao
    template_name = 'operacao/list.html'
    context_object_name = 'lists'
    ordering = '-data_operacao'
    paginate_by = 20

    def get_queryset(self):
        queryset = cache.get('operacao_listagem')  #recuperando dados no cache
               
        if not queryset:  # verificando se ha dados no chace. se nao tiver, buscar no banco de daos
            # Filtra as operações pelo usuário logado
            queryset = Operacao.objects.filter(fk_user_id=self.request.user.id,).order_by(self.ordering)
            cache.set('produtos_listagem', queryset, timeout=300)  # salva dados no cache
        
        # Aplica o filtro adicional caso tenha sido fornecido um nome (parâmetro GET)
        filter_name = self.request.GET.get('name')
        if filter_name:
            queryset = queryset.filter(ticket__icontains=filter_name)
        return queryset

    
#CRETE
class CadastroOperacao(SuccessMessageMixin, CreateView):
    model = Operacao
    form_class = OperacaoForm
    template_name = 'operacao/forms.html'
    success_url = reverse_lazy('list_operacao')
    success_message = 'Cadastro realizado com sucesso'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.fk_user = self.request.user  # Define o usuário autenticado
        object.ano = datetime.now().year
        cache.delete('operacao_listagem')  # Limpa o cache
        object.save()
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 
    
#UPDATE
class OperacaoUpdate(SuccessMessageMixin, UpdateView):
    model = Operacao
    template_name ='operacao/forms.html'
    form_class = OperacaoForm
    success_url = reverse_lazy('list_operacao')
    success_message ='Atualizada realizado com sucesso'
    
    def form_valid(self, form):
        object = form.save(commit=False)
        cache.delete('operacao_listagem')  # Limpa o cache
        object.save()
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url)
    
    

#DELETE
class OperacaoDelete( SuccessMessageMixin, DeleteView):
    model=Operacao
    success_url = reverse_lazy('list_operacao')
    success_message='Cadastro excluído com sucesso.'
    
