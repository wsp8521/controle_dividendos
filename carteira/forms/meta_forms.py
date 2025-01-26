from django import forms
from carteira import models
        

        
########################################## SETOR ###################################################   
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

