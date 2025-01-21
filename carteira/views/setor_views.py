
from carteira.models import SetorAtivo
from django.urls import reverse_lazy
from carteira.forms import SetorForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView



#CRETE
class CadastroSetor(SuccessMessageMixin, CreateView):
    model = SetorAtivo
    form_class = SetorForm
    template_name = 'setor/forms.html'
    success_url = reverse_lazy('list_ativo')
    success_message = 'Cadastro realizado com sucesso'

    