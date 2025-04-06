import json
import locale
from django.shortcuts import render
from carteira import metrics_charts


def desh(request):
    id_user = request.user.id  # ID do usuário autenticado
    filter = request.GET.get('ativo') if request.GET.get('ativo') else "FII"
    patrimonio_por_classe = metrics_charts.metrica_patrimonio(id_user)["patrimonio_por_classe"]
    render_grafico = True  # Ou False, se não for a página que deve renderizar o gráfico
    context = {
        #dados para os gráficoos 
        'ativo_por_classe': json.dumps(metrics_charts.grafico_ativo_por_classe(id_user)),  # Converte para JSON
        'ativo_por_setor': json.dumps(metrics_charts.grafico_ativo_por_setor(id_user,filter)), 
        'patrimonio': json.dumps({
            "classe": list(patrimonio_por_classe.keys()),  # Converte para JSON
            "valores": list(patrimonio_por_classe.values()),
    
            }),  
        'proventos_mensais': json.dumps(metrics_charts.grafico_proventos_mensais(id_user)),  # Converte para JSON
        'composicao_dividendos': json.dumps(metrics_charts.grafico_composicao_dividendos(id_user)),  # Converte para JSON
    
        #dados de metricas
        'metricas_patrimonio':metrics_charts.metrica_patrimonio(id_user),
        'metricas_dividendos': metrics_charts.metrica_dividendos(id_user),  # Adicionei a métrica de dividendos aqui    
        
        #variaveis de controle
        'render_grafico': render_grafico  # Variável de controle para renderizar o script javaScript
    }
   
    print(context['metricas_dividendos'])  # Verifique se agora está correto
    return render(request, 'home/home.html', context)


