import json
import locale
from datetime import datetime
from django.db.models import Q, Sum
from carteira.forms import PlanForm
from django.core.cache import cache
from django.urls import reverse_lazy
from django.http import JsonResponse
from utils.cotacao import obter_cotacao
from decimal import Decimal, InvalidOperation
from utils.media_dividendos import media_dividendos
from django.views.generic import ListView, DeleteView, CreateView
from carteira.models import PlanMetas, PrecoTeto, Ativos, MetaAtivo, Operacao
from django.contrib import messages
from django.shortcuts import get_object_or_404

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Class to Render the List of Financial Goals
class PlanMetasRender(ListView):
    model = PlanMetas
    template_name = 'plan_metas/list.html'
    context_object_name = 'lists'
    paginate_by = 10

    def get_queryset(self):
        filter = self.request.GET.get('classe')
        queryset = PlanMetas.objects.filter(fk_user_id=self.request.user.id).order_by('id_ativo')
        filter_ano = self.request.GET.get('ano')  # Captura o ano do filtro
        ano_atual = datetime.now().year

        if filter:
            queryset = queryset.filter(classe__icontains=filter)
            
        if filter_ano:
            queryset = queryset.filter(ano=filter_ano)  # Aplica o filtro de ano selecionado
        else:
            queryset = queryset.filter(ano=ano_atual)  # Aplica o filtro de ano atual       
        return queryset
    
    def get_context_data(self, **kwargs):
        plan_metas = self.get_queryset()
        context = super().get_context_data(**kwargs)
        anos_lista = PlanMetas.objects.filter(fk_user_id=self.request.user.id).values_list('ano', flat=True).distinct().order_by('-ano')
        meta_ativo = MetaAtivo.objects.filter(fk_user_id=self.request.user.id, ano=datetime.now().year)
        operacao = Operacao.objects.filter(fk_user_id=self.request.user.id)
        filter_status = self.request.GET.get('status')  # Pega o filtro de status da URL
        filter_ano = self.request.GET.get('ano') if self.request.GET.get('ano') else datetime.now().year
        filter_classe = self.request.GET.get('classe')  # Captura a classe do filtro no template
        filter_recomendacao = self.request.GET.get('recomendacao')  # Filtro para recomendação
        filter_ativo = Q(ano=filter_ano) if filter_classe is None else Q(ano=filter_ano) & Q(classe=filter_classe)
        lista_ativos = []
        tickers = [ativo.id_ativo for ativo in plan_metas]
        
        # Recupera os dados do cache que foi setado na função obter_cotacao
        cotacoes = obter_cotacao(tickers)
        
        # Busca médias de dividendos de uma só vez para evitar múltiplas chamadas
        dividendos_cache = {ativo.id_ativo: media_dividendos(self.request.user.id,ativo.id_ativo, ativo.classe, 5) for ativo in plan_metas}
        
        for plan in plan_metas:
            get_preco_teto = PrecoTeto.objects.filter(id_ativo=plan.id_ativo).first()
            ativos = Ativos.objects.filter(ticket=plan.id_ativo).first()
            cota_restante = plan.qtd - ativos.qtdAtivo if (plan.qtd - ativos.qtdAtivo) > 0 else 0
            cotacao = cotacoes.get(plan.id_ativo) if cotacoes else None
                    
            # Busca no dicionário dividendos_cache pelo valor associado à chave ativo.id_ativo.
            dividendos = dividendos_cache.get(plan.id_ativo, Decimal(0))
            rentabilidade = Decimal(get_preco_teto.rentabilidade) if get_preco_teto and get_preco_teto.rentabilidade else 0
            preco_teto_acoes = Decimal(dividendos) / (Decimal(rentabilidade) / Decimal(100)) if rentabilidade != 0 else 0
            ipca = Decimal(get_preco_teto.ipca) if get_preco_teto and get_preco_teto.ipca else Decimal(0)
            preco_teto_fii = (Decimal(dividendos) / (ipca + rentabilidade)) * 100 if rentabilidade != 0 else 0
            preco_teto = preco_teto_acoes if plan.classe == "Ação" else preco_teto_fii
            diferenca = Decimal(cotacao or 0) - preco_teto
            if cotacao is not None:
                total = Decimal(cotacao) * cota_restante if cota_restante > 0 else 0
            else:
                total = 0
            recomendacao = "Comprar" if diferenca < 0 else "Não comprar"
            
            if plan.qtd == ativos.qtdAtivo:
                status_meta = 1  # Alcançada
            elif ativos.qtdAtivo > plan.qtd:
                status_meta = 2  # Ultrapassada
            else:
                status_meta = 0  # Não alcançada
                
            lista_ativos.append({
                "pk": plan.id,
                "ativo": plan.id_ativo,
                "qtd": plan.qtd,
                "classe": plan.classe,
                "cota_restante": cota_restante,
                "qtd_atual": ativos.qtdAtivo,
                "rentabilidade": rentabilidade,
                "cotacao": cotacao,
                "preco_teto": preco_teto,
                "diferenca": diferenca,
                "recomendacao": recomendacao,
                "status": status_meta,
                "total": total,
                "ano": plan.ano
            })
        
        # Aplicando o filtro de status
        if filter_status:
            lista_ativos = [item for item in lista_ativos if item["status"] == filter_status]
                
        if filter_recomendacao:
            lista_ativos = [item for item in lista_ativos if item["recomendacao"] == filter_recomendacao]
            
        # Obtendo total necessário para investimento
        investimento_total = sum(item["total"] for item in lista_ativos)

        # Ordena os anos em ordem decrescente
        anos_unicos = sorted(set(anos_lista), reverse=True)
        
        if meta_ativo.filter(filter_ativo):  # Verifica se há metas do ano cadastrado
            meta_geral = meta_ativo.filter(filter_ativo).aggregate(Sum("meta_geral"))['meta_geral__sum']
            meta_anual = meta_ativo.filter(filter_ativo).aggregate(Sum("meta_anual"))['meta_anual__sum']
            meta_alcancada = operacao.filter(filter_ativo & ~Q(tipo_operacao="Venda")).aggregate(Sum("qtd"))['qtd__sum'] or 0
            meta_status = f"Falta {meta_anual-meta_alcancada}" if meta_anual-meta_alcancada >= 0 else f'Superado {(meta_anual-meta_alcancada)*-1}'
        else:
            meta_geral = 0
            meta_anual = 0
            meta_alcancada = 0
            meta_status = 0
            
            messages.error(self.request, "Nenhuma meta encontrada para o ano selecionado.")
        
        context['ano_atual'] = datetime.now().year
        context['investimento_total'] = locale.currency(investimento_total, grouping=True) if investimento_total else 0
        context['meta_geral'] = meta_geral
        context['meta_anual'] = meta_anual
        context['meta_alcancada'] = meta_alcancada
        context['meta_status'] = meta_status
        context['lists'] = lista_ativos
        context['is_meta_ativos'] = True if meta_ativo else False
        context['anos_disponiveis'] = anos_unicos  # Passando anos agrupados para o template
        


        return context


# Class to Handle the Creation of New Financial Goals
class CadastroPlan(CreateView):
    model = PlanMetas
    form_class = PlanForm
    template_name = 'plan_metas/forms.html'
    success_url = reverse_lazy('list_plan')
    success_message = 'Cadastro realizado com sucesso'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_classe = MetaAtivo.objects.filter(fk_user_id=self.request.user.id, ano=datetime.now().year)
        context['filter_classe'] = list(filter_classe.values_list('classe', flat=True).distinct()) 
        return context
    

    def form_valid(self, form):
        object = form.save(commit=False)
        object.fk_user = self.request.user  # Define o usuário autenticado
        object.ano = datetime.now().year         
        object.save()
        return super().form_valid(form)  # Redireciona o usuário para a URL de sucesso definida (success_url) 
 

# Function to Handle Updates to Active Quantities
def update_qtd_ativo(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Obtém os dados passados no JavaScript
            meta = get_object_or_404(PlanMetas, id=pk)  # Obtém o objeto PlanMetas
                    
            # Atualiza os dados da PlanMetas
            if "qtd" in data:
                meta.qtd = int(data["qtd"])
            if "qtd_calc" in data:
                meta.qtd_calc = int(data["qtd_calc"])

            if "proventos" in data:
                try:
                    proventos = data["proventos"].strip().replace(",", ".")
                    meta.prov_cota = Decimal(proventos)
                except (InvalidOperation, ValueError):
                    return JsonResponse({"status": "error", "message": "Valor inválido para proventos"}, status=400)
                
            # Salva as alterações na PlanMetas
            meta.save()

            return JsonResponse({"status": "success", "message": "Metas e investimento atualizados com sucesso!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Método inválido!"}, status=400)


# Class to Handle Deleting Financial Goals
class PlanDelete(DeleteView):
    model = PlanMetas
    success_url = reverse_lazy('list_plan')
    success_message = 'Cadastro excluído com sucesso.'
