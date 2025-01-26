from django.db.models import Sum, Q
from carteira.models import MetaAtivo
from django.urls import reverse_lazy
from carteira.forms import MetaForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView




#READ
class MetaRender(ListView):
    model = MetaAtivo
    template_name = 'metas_geral/list.html'
    context_object_name = 'lists'
    ordering = '-ano'
    paginate_by = 10
    
    def get_queryset(self):
        return MetaAtivo.objects.filter(fk_user=self.request.user).order_by("-ano")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtra os dados por classe
        context["metas_fii"] = self.get_queryset().filter(classe="FII")
        context["metas_acoes"] = self.get_queryset().filter(classe="Ação")
        print("############################")
        print(context["metas_acoes"] )
        print("############################")
        
        return context
    
# #CRETE
class CadastroMetas(SuccessMessageMixin, CreateView):
    model = MetaAtivo
    form_class = MetaForm
    template_name = 'metas_geral/forms.html'
    success_url = reverse_lazy('list_metas')
    success_message = 'Cadastro realizado com sucesso'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.fk_user = self.request.user  # Define o usuário autenticado
        
        
        # Calcula a soma das metas anuais dos anos anteriores
        meta_anual_anterior = MetaAtivo.objects.filter(
            fk_user=self.request.user,
            classe=object.classe
        ).aggregate(Sum('meta_alcancada'))['meta_alcancada__sum'] or 0
        
         #calculo da meta do ano anterior
        meta_anterior = MetaAtivo.objects.filter(
            fk_user=self.request.user, 
            ano = object.ano-1,
            classe = object.classe,
        ).aggregate(Sum('meta_geral_alcancada'))['meta_geral_alcancada__sum'] or 0

        object.meta_geral_alcancada = meta_anual_anterior 
        object.meta_geral = meta_anterior + object.meta_anual
    
        object.save()
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 
    
#UPDATE
class MetasUpdate(SuccessMessageMixin, UpdateView):
    model = MetaAtivo
    template_name ='metas_geral/forms.html'
    form_class = MetaForm
    success_url = reverse_lazy('list_metas')
    success_message ='Atualizada realizado com sucesso'
    
       
    def form_valid(self, form):
        object = form.save(commit=False)
        object.fk_user = self.request.user  # Define o usuário autenticado
        
        
        # Calcula a soma das metas anuais dos anos anteriores
        meta_anual_anterior = MetaAtivo.objects.filter(
            fk_user=self.request.user, 
            classe=object.classe
        ).aggregate(Sum('meta_alcancada'))['meta_alcancada__sum'] or 0
        
        #calculo da meta do ano anterior
        meta_anterior = MetaAtivo.objects.filter(
            fk_user=self.request.user, 
            ano = object.ano-1,
            classe = object.classe,
        ).aggregate(Sum('meta_geral_alcancada'))['meta_geral_alcancada__sum'] or 0

        object.meta_geral_alcancada = meta_anual_anterior 
        object.meta_geral = meta_anterior + object.meta_anual
    
        object.save()
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 
    

#DELETE
class MetasDelete( SuccessMessageMixin, DeleteView):
    model=MetaAtivo
    success_url = reverse_lazy('list_metas')
    success_message='Cadastro excluído com sucesso.'