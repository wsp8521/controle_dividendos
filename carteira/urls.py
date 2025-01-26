from django.urls import path
from carteira import views

urlpatterns = [


    #CRUD ATIVO
    path('ativo/', views.AtivoRender.as_view(), name='list_ativo'),
    path('ativo/create', views.CadastroAtivos.as_view(), name='create_ativo'),
    path('ativo/update/<int:pk>', views.AtivosUpdate.as_view(), name='update_ativo'),
    path('ativo/delete/<int:pk>', views.AtivoDelete.as_view(), name='delete_ativo'),
    
    #CRUD OPERACAO
    path('operacao/', views.OperacaoRender.as_view(), name='list_operacao'),
    path('operacao/create', views.CadastroOperacao.as_view(), name='create_operacao'),
    path('operacao/update/<int:pk>', views.OperacaoUpdate.as_view(), name='update_operacao'),
    path('operacao/delete/<int:pk>', views.OperacaoDelete.as_view(), name='delete_operacao'),
    
    
    #CRUD PROVENTOS
    path('proventos/', views.ProventosRender.as_view(), name='list_proventos'),
    path('proventos/create', views.CadastroProventos.as_view(), name='create_proventos'),
    path('proventos/update/<int:pk>', views.ProventosUpdate.as_view(), name='update_proventos'),
    path('proventos/delete/<int:pk>', views.ProventosDelete.as_view(), name='delete_proventos'),
    
    #CRUD META
    path('metas/', views.MetaRender.as_view(), name='list_metas'),
    path('metas/create', views.CadastroMetas.as_view(), name='create_metas'),
    path('metas/update/<int:pk>', views.MetasUpdate.as_view(), name='update_metas'),
    path('metas/delete/<int:pk>', views.MetasDelete.as_view(), name='delete_metas'),
    
    #CRUD PRECO TETO
    path('preco/', views.PrecoTetoRender.as_view(), name='list_preco_teto'),
    path('metas/create', views.CadastroMetas.as_view(), name='create_metas'),
    path('metas/update/<int:pk>', views.MetasUpdate.as_view(), name='update_metas'),
    path('metas/delete/<int:pk>', views.MetasDelete.as_view(), name='delete_metas'),
    
    
    
    
    
    #CRUD SETOR
    path('setor/create', views.CadastroSetor.as_view(), name='create_setor'),
    
    #CRUD desh
    path('', views.desh, name='desh'),
]