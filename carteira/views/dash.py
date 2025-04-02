import json

from django.shortcuts import render

from carteira import metrics_charts
import json  # Adicione essa importação


def desh(request):
    filter = request.GET.get('ativo') if request.GET.get('ativo') else "FII"
    render_grafico = True  # Ou False, se não for a página que deve renderizar o gráfico
    id_user = request.user.id  # ID do usuário autenticado
    context = {
        #dados para os gráficoos 
        'ativo_por_classe': json.dumps(metrics_charts.ativo_por_classe(id_user)),  # Converte para JSON
        'ativo_por_setor': json.dumps(metrics_charts.ativo_por_setor(id_user,filter)),  
        'patrimonio': json.dumps(metrics_charts.patrimonio(id_user)["patrimonio_por_classe"]),  # Apenas a chave desejada
        
        #dados de metricas


        
        #
        'render_grafico': render_grafico  # Variável de controle para renderizar o script javaScript
    }
   
    #print(context['patrimonio']['patrimonio_por_classe'])  # Verifique se agora está correto
    return render(request, 'dash/dash.html', context)


