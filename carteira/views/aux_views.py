from carteira.models import SetorAtivo, Ativos
from django.http import JsonResponse
from utils.cotacao import obter_cotacao
from django.core.cache import cache

#FUNÇÕES GERAIS
def atualizar_cotacao(request):
    """Remove os dados do cache e busca novas cotações."""
    cache_key = "cotacao_key"
    
    # Obtém os ativos do usuário logado
    ativos = Ativos.objects.filter(fk_user_id=request.user.id)
    tickers = [ativo.ticket for ativo in ativos]

    # Força a atualização das cotações
    novas_cotacoes = obter_cotacao(tickers)
    cache.set(cache_key, novas_cotacoes, timeout=600)  # Armazena por 10 minutos
    return JsonResponse({"status": "success", "mensagem": "Cotações atualizadas com sucesso!"})


#funççao que filtra o setor por classe no formulario cadastro de ativos
def get_setores_por_classe(request):
    classe = request.GET.get('classe')
    user = request.user
    setores = SetorAtivo.objects.filter(fk_user=user, setor_classe=classe).values('id', 'setor')
    setores = SetorAtivo.objects.filter(setor_classe=classe).values('id', 'setor')

    return JsonResponse(list(setores), safe=False)


def filtrar_ativos(request):
    classe = request.GET.get('classe', '')
    
    # Filtra os ativos com base na classe
    ativos = Ativos.objects.filter(classe=classe, fk_user_id=request.user.id,)
    
    # Prepara a resposta em formato JSON
    ativos_data = [{'id': ativo.pk, 'nome': ativo.ticket} for ativo in ativos]
    print(ativos_data)
    return JsonResponse({'ativos': ativos_data})