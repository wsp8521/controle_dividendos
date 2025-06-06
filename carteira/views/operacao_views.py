from datetime import datetime
from calendar import month_name
from django.core.cache import cache
from django.urls import reverse_lazy
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
        queryset = cache.get('operacao_listagem')
        self.filter_url_pag_nav = ""

        # Filtros
        filter_ativo = self.request.GET.get('ativo')
        filter_classe = self.request.GET.get('classe_ativos')
        filter_operacao = self.request.GET.get('operacao')
        filter_mes = self.request.GET.get('mes')
        filter_ano = self.request.GET.get('anos')

        # Se cache não existir, buscar do banco
        if not queryset:
            queryset = Operacao.objects.filter(
                fk_user_id=self.request.user.id
            ).order_by(self.ordering)
            cache.set('operacao_listagem', queryset, timeout=300)

        # Aplicando os filtros (e montando url + dicionário para exibir no template)
        if filter_ativo:
            queryset = queryset.filter(id_ativo__ticket__icontains=filter_ativo)
            self.filter_url_pag_nav += f"&ativo={filter_ativo}"

        if filter_classe:
            queryset = queryset.filter(classe=filter_classe)
            self.filter_url_pag_nav += f"&classe_ativos={filter_classe}"

        if filter_operacao:
            queryset = queryset.filter(tipo_operacao=filter_operacao)
            self.filter_url_pag_nav += f"&operacao={filter_operacao}"
           
        if filter_mes:
            queryset = queryset.filter(mes=filter_mes)
            self.filter_url_pag_nav += f"&mes={filter_mes}"
            
        if filter_ano:
            queryset = queryset.filter(ano=filter_ano)
            self.filter_url_pag_nav += f"&anos={filter_ano}"
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']
        list_operacao = page_obj.object_list
        meses = [(i, month_name[i]) for i in range(1, 13)]
        anos = Operacao.objects.filter(fk_user_id=self.request.user.id).values_list('ano', flat=True).distinct().order_by('-ano')

        context['lists'] = list_operacao
        context['page_name'] = {'key':2,"page":"Operações"}
        context['meses'] = meses
        context['anos'] = anos

        # Passa os filtros para o template
        context['url_filter_pagination'] = self.filter_url_pag_nav or ""
   
        return context

    
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
    
