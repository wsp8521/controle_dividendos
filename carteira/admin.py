from django.contrib import admin
from carteira.models import Ativos, Proventos, Operacao, MetaAtivo, SetorAtivo

@admin.register(Ativos)
class AtivosAdmin(admin.ModelAdmin):
    list_display=("id","ativo", "ticket","classe", "created_at","update_at")
    list_display_links=("ativo",)
    
    
@admin.register(Proventos)
class ProventosAdmin(admin.ModelAdmin):
    list_display=("id", "ticket", "classe", "valor_recebido","data_pgto", "created_at","update_at")
    list_display_links=("ticket",)
    

@admin.register(Operacao)
class OperacaoAdmin(admin.ModelAdmin):
    list_display=("id", "ticket", "classe", "tipo_operacao","data_operacao", "qtd", "valor_cota", "valor_total", "created_at","update_at")
    list_display_links=("ticket",)
    

@admin.register(MetaAtivo)
class MetaAtivoAdmin(admin.ModelAdmin):
    list_display=("id", "ano", "qtd_fii", "qtd_acoes","total", "created_at","update_at")
    list_display_links=("ano",)
    
@admin.register(SetorAtivo)
class SetorAtivoAdmin(admin.ModelAdmin):
    list_display=("id", "setor","created_at","update_at")
    list_display_links=("setor",)
    