from django import forms
from carteira import models


########################################## DIVIDENDOS ###################################################  
class ProventosForm(forms.ModelForm):
    class Meta:
        model = models.Proventos
        fields = ['classe', 'ticket', 'tipo_provento', 'valor_recebido', 'data_pgto']
        widgets = {
            #'ticket': forms.TextInput(attrs={'class': 'form-control'}),
            'data_pgto': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',  # Usando texto para poder customizar o formato no frontend
                    'placeholder': 'dd/mm/aaaa',
                },
                format='%d/%m/%Y'  # Formato da data exibido no campo
            ),

            'valor_recebido': forms.NumberInput(
                attrs={
                        'class': 'form-control',
                        'step': '0.01',  # Permite valores decimais com precisão de centavos
                        'inputmode': 'decimal',  # Melhora a experiência do usuário para entrada de números decimais
                }), 
              
        }

    # Definindo as opções dos campos select
    
    classe_options = [
        (False, 'Classe do ativo'),
        ('Ação', 'Ação'),
        ('FII', 'FII'),
    ]
    
    op_options = [
        (False, 'Tipo de operação'),
        ('Dividendos', 'Dividendos'),
        ('JCP', 'JCP'),
    ]

    # Campos de escolha com widgets apropriados
    classe = forms.ChoiceField(choices=classe_options, widget=forms.Select(attrs={'class': 'form-control'}))
    tipo_provento = forms.ChoiceField(choices=op_options, widget=forms.Select(attrs={'class': 'form-control'}))
    ticket = forms.ChoiceField(
    choices=[(ativo.ticket, ativo.ticket) for ativo in models.Ativos.objects.all()],
    widget=forms.Select(attrs={'class': 'form-control'}),
    label="Ativo"
)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Verifica se a instância está sendo editada
        is_editing = self.instance and self.instance.pk

        # Lista de escolhas
        tickets = [(ativo.ticket, ativo.ticket) for ativo in models.Ativos.objects.all()]

        # Adiciona o item em branco apenas no modo de adição
        if not is_editing:
            tickets.insert(0, ("", "Selecione um ativo"))

        # Define as escolhas do campo ticket
        self.fields['ticket'].choices = tickets

    
