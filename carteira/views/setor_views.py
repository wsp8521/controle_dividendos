
from carteira.models import SetorAtivo
from django.urls import reverse_lazy
from carteira.forms import SetorForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.http import JsonResponse


#CRETE
class CadastroSetor(SuccessMessageMixin, CreateView):
    model = SetorAtivo
    form_class = SetorForm
    template_name = 'setor/forms.html'
    success_url = reverse_lazy('list_ativo')
    #success_message = 'Cadastro realizado com sucesso'
    
    def form_valid(self, form):
        object = form.save(commit=False)
        object.fk_user = self.request.user  # Define o usuário autenticado
        object.save()
        
        if self.request.headers.get('Hx-Request') == 'true':
            return JsonResponse({
                'id': object.id,
                'nome': object.setor,
                'mensagem': f'Setor "{object.setor}" cadastrado com sucesso!'
            })

        
        return super().form_valid(form) #redirecionar o usuário para a URL de sucesso definida (success_url) 

    