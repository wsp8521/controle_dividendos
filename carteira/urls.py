from django.urls import path
from carteira import views

urlpatterns = [
    
     #DESH
    path('', views.desh, name='desh'),
    
    #CRUD ATIVO
    path('ativo/', views.AtivoRender.as_view(), name='list_ativo'),
    path('ativo/detail/<int:pk>', views.AtivoDetail.as_view(), name='detail_ativo'),
    path('ativo/create', views.CadastroAtivos.as_view(), name='create_ativo'),
    path('ativo/update/<int:pk>', views.AtivosUpdate.as_view(), name='update_ativo'),
    path('ativo/delete/<int:pk>', views.AtivoDelete.as_view(), name='delete_ativo'),
    
    #atualizar contacao
    path("ativo/atualizar-cotacao/", views.atualizar_cotacao, name="atualizar_cotacao"),
    path('get-setores/', views.get_setores_por_classe, name='get_setores'),
    
    #CRUD OPERACAO
    path('operacao/', views.OperacaoRender.as_view(), name='list_operacao'),
    path('operacao/create', views.CadastroOperacao.as_view(), name='create_operacao'),
    path('operacao/update/<int:pk>', views.OperacaoUpdate.as_view(), name='update_operacao'),
    path('operacao/delete/<int:pk>', views.OperacaoDelete.as_view(), name='delete_operacao'),
    path('operacao/filtrar-ativos/', views.filtrar_ativos, name='filtrar_ativos'),
    
    
    #CRUD PROVENTOS
    path('proventos/', views.ProventosRender.as_view(), name='list_proventos'),
    path('proventos/create', views.CadastroProventos.as_view(), name='create_proventos'),
    path('proventos/update/<int:pk>', views.ProventosUpdate.as_view(), name='update_proventos'),
    path('proventos/delete/<int:pk>', views.ProventosDelete.as_view(), name='delete_proventos'),
    
    #operaçao com proventos
    path('proventos/filtrar-ativos/', views.filtrar_ativos, name='filtrar_ativos'),
    path('proventos/agenda/', views.pgto_proventos, name='pgto_proventos'),
    path('proventos/pesquisar/', views.pesquisar_pagamento, name='pesquisar_proventos'),
    path('status-tarefa/<str:task_id>/', views.verificar_status_tarefa, name='verificar_status_tarefa'),
    
    #CRUD META
    path('metas/', views.MetaRender.as_view(), name='list_metas'),
    path('metas/create', views.CadastroMetas.as_view(), name='create_metas'),
    path('metas/update/<int:pk>', views.MetasUpdate.as_view(), name='update_metas'),
    path('metas/delete/<int:pk>', views.MetasDelete.as_view(), name='delete_metas'),
    
    #CRUD PLANO DE METAS
    path('plan-metas/', views.PlanMetasRender.as_view(), name='list_plan'),
    path('plan-metas/create', views.CadastroPlan.as_view(), name='create_plan'),
    path('plan-metas/delete/<int:pk>', views.PlanDelete.as_view(), name='delete_plan'),
    path('plan-metas/update/<int:pk>', views.update_qtd_ativo, name='update_plan'),
    path('plan-metas/filtrar-ativos/', views.filtrar_ativos, name='filtrar_plan'),
    
    #calculadaora
    path('plan-metas/calculadora/', views.calculadora_ativos, name='calculadora_plan'),
    path('plan-metas/calculadora/investimento/', views.create_valor_investido, name='create_investimento'),
    path('plan-metas/calculadora/<int:pk>', views.update_valor_investido, name='calc_investimento'),
    
    #CRUD PRECO TETO
    path('preco/', views.PrecoTetoRender.as_view(), name='list_preco_teto'),
    #path('preco/detail/<int:pk>', views.PrecoTetoDetail.as_view(), name='detail_preco_teto'),   
    path('preco/create', views.CadastroPrecoTeto.as_view(), name='create_preco_teto'),
    path('preco/update/<int:pk>', views.PrecoTetoUpdate.as_view(), name='update_preco_teto'),
    path('preco/delete/<int:pk>', views.PrecoTetoDelete.as_view(), name='delete_preco_teto'),
    path('preco/filtrar-ativos/', views.filtrar_ativos, name='filtrar_ativos'),
    
    
    #CRUD SETOR
    path('setor/create', views.CadastroSetor.as_view(), name='create_setor'),
    
]