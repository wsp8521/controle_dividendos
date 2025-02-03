from django import forms
from carteira import models
        
########################################## ATIVOS ###################################################  
class AtivosForm(forms.ModelForm):
    class Meta:
        model = models.Ativos
        fields=['ativo','ticket','classe','cnpj','setor','qtdAtivo','investimento','dividendos']
        widgets={
            'ativo':forms.TextInput(attrs={'class':'form-control'}), #alterando atribuutos do campo
            'ticket':forms.TextInput(attrs={'class':'form-control'}),
            'cnpj':forms.TextInput(attrs={'class':'form-control'}),
            'qtdAtivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'dividendos': forms.NumberInput(attrs={'class': 'form-control'}),
            'investimento': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    classe_options = [
         (False, 'Classe do ativo'),
        ('Ação', 'Ação'),
        ('FII', 'FII'),
        ('FII-Infra', 'FII-Infra'),
    ]
    
    classe = forms.ChoiceField(choices=classe_options, widget=forms.Select(attrs={'class': 'form-control'}))
    
     # Definindo o campo setor como um ModelChoiceField que busca dados da tabela Setor
    setor = forms.ModelChoiceField(
        queryset=models.SetorAtivo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Selecione o setor",
       
    )
        
    def __init__(self, *args, **kwargs):
        is_edit = kwargs.pop('is_edit', False)  # Parâmetro extra para verificar o contexto (adição ou edição de registro)
        super().__init__(*args, **kwargs)
   
        # Remove os campos que não devem aparecer no formulário no modo adição
        if not is_edit:
            for field in ['qtdAtivo', 'dividendos', 'investimento']:
                self.fields.pop(field)
        
########################################## SETOR ###################################################   
class SetorForm(forms.ModelForm):
    class Meta:
        model = models.SetorAtivo
        fields=['setor','setor_classe']
        widgets={
            'setor':forms.TextInput(attrs={'class':'form-control'}), #alterando atribuutos do campo
        }
            
    classe_options = [
         (False, 'Classe do ativo'),
        ('Ação', 'Ação'),
        ('FII', 'FII'),
        ('FII-Infra', 'FII-Infra'),
    ]
    
    setor_classe = forms.ChoiceField(choices=classe_options, widget=forms.Select(attrs={'class': 'form-control'}))

########################################## OPERACAO ###################################################  
class OperacaoForm(forms.ModelForm):
    class Meta:
        model = models.Operacao
        fields = ['classe', 'id_ativo', 'tipo_operacao', 'data_operacao', 'qtd', 'valor_cota', 'fonte_recurso']
        widgets = {
            #'ticket': forms.TextInput(attrs={'class': 'form-control'}),
            'data_operacao': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',  # Usando texto para poder customizar o formato no frontend
                    'placeholder': 'dd/mm/aaaa',
                },
                format='%d/%m/%Y'  # Formato da data exibido no campo
            ),
            'qtd': forms.NumberInput(attrs={'class': 'form-control'}),  # Usando NumberInput
            'valor_cota': forms.NumberInput(
                attrs={
                        'class': 'form-control',
                        'step': '0.01',  # Permite valores decimais com precisão de centavos
                        'inputmode': 'decimal',  # Melhora a experiência do usuário para entrada de números decimais
                }), 
            
            'valor_total': forms.NumberInput(
                attrs={
                        'class': 'form-control',
                        'step': '0.01', 
                        'inputmode': 'decimal',  
                }),
            
             'id_ativo':forms.Select(attrs={'class': 'form-control'})
        }
        

    # Definindo as opções dos campos select
      
    classe_options = [
         (False, 'Classe do ativo'),
        ('Ação', 'Ação'),
        ('FII', 'FII'),
        ('FII-Infra', 'FII-Infra'),
    ]
    
    font_recuso=[
        (False, 'Fonte de recurso'),
        ('Aporte', 'Aporte'),
        ('Bonificação', 'Bonificação'),
        ('Dividendos', 'Dividendos'),
    ]
    
    op_options = [
        (False, 'Tipo de operação'),
        ('Compra', 'Compra'),
        ('Venda', 'Venda'),
        ('Bonificação', 'Bonificação'),
        ('Dação', 'Dação'),
        ('Desdobramento', 'Desdobramento'),
    ]

    # Campos de escolha com widgets apropriados
    classe = forms.ChoiceField(
        choices=classe_options, 
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'onchange':"filtrarAtivos('/operacao')"
                
                }),
            required=True, error_messages={'required': 'Este campo é obrigatório.'  # Mensagem de erro personalizada
            }
        
        )
    tipo_operacao = forms.ChoiceField(choices=op_options, widget=forms.Select(attrs={'class': 'form-control'}))
    fonte_recurso = forms.ChoiceField(choices=font_recuso, widget=forms.Select(attrs={'class': 'form-control'}))
   
 

