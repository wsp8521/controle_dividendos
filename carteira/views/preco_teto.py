import json
from carteira.models import PrecoTeto
from django.urls import reverse_lazy
from carteira.forms import AtivosForm
from utils.cotacao import obter_cotacao
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView


#READ
class PrecoTetoRender(ListView):
    model = PrecoTeto
    template_name = 'preco_teto/list.html'
    context_object_name = 'lists'
    paginate_by = 10

    def get_queryset(self):
        filter_name = self.request.GET.get('name')
        queryset = PrecoTeto.objects.all().order_by('id_ativo')
        if filter_name:
            return PrecoTeto.objects.filter(classe__icontains=filter_name)
        return queryset 
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ativos = self.get_queryset()
        lista_ativos = []
        
        for ativo in ativos:
            cotacao = obter_cotacao(ativo.id_ativo)
            lista_ativos.append({
                "ativo": ativo.id_ativo,
                "classe": ativo.classe,
                "rentabilidade":ativo.rentabilidade,
                "ipca": ativo.ipca if ativo.ipca is not None else 0,
                "cotacao": cotacao,
            })

        #Serializa a lista de ativos como JSON
        context['lists'] = lista_ativos
        return context
    
    
# #CRETE
# class CadastroAtivos(SuccessMessageMixin, CreateView):
#     model = Ativos
#     form_class = AtivosForm
#     template_name = 'ativos/forms.html'
#     success_url = reverse_lazy('list_ativo')
#     success_message = 'Cadastro realizado com sucesso'

#     def form_valid(self, form):
#         object = form.save(commit=False)
#         object.fk_user = self.request.user  # Define o usuário autenticado
#         object.save()
#         return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 
    
# #UPDATE
# class AtivosUpdate(SuccessMessageMixin, UpdateView):
#     model = Ativos
#     template_name ='ativos/forms.html'
#     form_class = AtivosForm
#     success_url = reverse_lazy('list_ativo')
#     success_message ='Atualizada realizado com sucesso'
   
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['is_edit'] = True  # Passa o parâmetro is_edit=True para o formulário
#         return kwargs
    
# #DELETE
# class AtivoDelete( SuccessMessageMixin, DeleteView):
#     model=Ativos
#     success_url = reverse_lazy('list_ativo')
#     success_message='Cadastro excluído com sucesso.'
    
