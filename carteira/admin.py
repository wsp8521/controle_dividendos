from django.contrib import admin
from carteira.models import Ativos, Proventos, Operacao, MetaAtivo, SetorAtivo

@admin.register(Ativos)
class AtivosAdmin(admin.ModelAdmin):
    list_display=("id","ativo", "ticket","classe", "created_at","update_at")
    list_display_links=("ativo",)
    
    
@admin.register(Proventos)
class ProventosAdmin(admin.ModelAdmin):
    list_display=("id", "id_ativo", "classe", "valor_recebido","data_pgto", "created_at","update_at")
    list_display_links=("id_ativo",)
    

@admin.register(Operacao)
class OperacaoAdmin(admin.ModelAdmin):
    list_display=("id", "id_ativo", "classe", "tipo_operacao","data_operacao", "qtd", "valor_cota", "valor_total", "created_at","update_at")
    list_display_links=("id_ativo",)
    

@admin.register(MetaAtivo)
class MetaAtivoAdmin(admin.ModelAdmin):
    list_display=("id","classe","ano","meta_anual","meta_alcancada","meta_geral","meta_geral_alcancada" )
    list_display_links=("ano",)
    
@admin.register(SetorAtivo)
class SetorAtivoAdmin(admin.ModelAdmin):
    list_display=("id", "setor","created_at","update_at")
    list_display_links=("setor",)
    