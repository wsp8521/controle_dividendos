from django import forms
from carteira import models
        

        
########################################## METAS ANUAIS ###################################################   
class MetaForm(forms.ModelForm):
    class Meta:
        model = models.MetaAtivo
        fields=['ano','classe', 'meta_anual']
        widgets={
            'ano':forms.NumberInput(attrs={'class':'form-control'}),
            'meta_anual':forms.NumberInput(attrs={'class':'form-control'}),
        }
        
        
    classe_options = [
         (False, 'Classe do ativo'),
        ('Ação', 'Ação'),
        ('FII', 'FII'),
    ]
    
    classe = forms.ChoiceField(choices=classe_options, widget=forms.Select(attrs={'class': 'form-control'}))
    meta_anual = forms.IntegerField(label="Meta do Ano", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
########################################## PLANO DE METAS ###################################################   
class PlanForm(forms.ModelForm):
    class Meta:
        model = models.PlanMetas
        fields = ['classe', 'id_ativo', 'qtd']
        labels = {
            'qtd': 'Qtde+',  
        }
        widgets={'qtd':forms.NumberInput(attrs={'class':'form-control'})}
        
        
    classe_options = [
         (False, 'Classe do ativo'),
        ('Ação', 'Ação'),
        ('FII', 'FII'),
        ('FII-Infra', 'FII-Infra'),
        ('FII-Agro', 'FII-Agro'),
    ]
    
    classe = forms.ChoiceField(choices=classe_options, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name':'classe',
        

            }
        ))
    
####################################### PREÇO TETO #############################################    
class PrecoTetoForms(forms.ModelForm):
    class Meta:
        model = models.PrecoTeto
        fields = ['classe', 'id_ativo', 'rentabilidade', "ipca"]
        labels = {
            'ipca': 'IPCA+',  # Novo label para o campo ipca
        }
        widgets = {
            'rentabilidade': forms.NumberInput(
                attrs={
                        'class': 'form-control',
                        'step': '0.01',
                        'inputmode': 'decimal',
                }), 
            'ipca': forms.NumberInput(
                attrs={
                        'class': 'form-control',
                        'step': '0.01', 
                        'inputmode': 'decimal',  
                }),
            'id_ativo': forms.Select(attrs={
                'class': 'form-control',
                'id':'list_ativo'
                })
        }

    # Definindo as opções dos campos select    
    classe_options = [
        (False, 'Classe do ativo'),
        ('Ação', 'Ação'),
        ('FII', 'FII'),
      ('FII-Infra', 'FII-Infra'),
      ('FII-Agro', 'FII-Agro'),
    ]
    
    # Campos de escolha com widgets apropriados
    classe = forms.ChoiceField(choices=classe_options, widget=forms.Select(
        attrs={
            'class': 'form-control'}
        ))
    


