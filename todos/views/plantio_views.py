from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from datetime import timedelta, timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.utils.timezone import now
import pytz
from django.db.models import Prefetch, CharField, Value, Subquery, OuterRef, Q

from todos.views.excel_views import export_to_excel

from ..models import AtividadeP, ManejoProduto, Plantio, Manejo, Produtos, TipoAplicacao
from ..forms import PlantioForm

class PlantioListView(ListView):
    model = Plantio
    success_url = reverse_lazy("plantio_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manejos"] = Manejo.objects.all()
        return context

class PlantioCreateView(CreateView):
    model = Plantio
    form_class = PlantioForm
    success_url = reverse_lazy("plantio_list")

    def form_valid(self, form):
        form.instance.data_criada = now()
        form.instance.save(using="default")
        return super().form_valid(form)


class PlantioUpdateView(UpdateView):
    model = Plantio
    form_class = PlantioForm
    success_url = reverse_lazy("plantio_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['data_plantio'].widget.format = '%Y-%m-%d'
        return form


class PlantioDeleteView(DeleteView):
    model = Plantio
    
    
@csrf_exempt
def plantio_view(request, pk):
    plantio = get_object_or_404(Plantio, pk=pk)
    atividades = AtividadeP.objects.all()
    tipos_aplicacao = TipoAplicacao.objects.all()

    produto_subquery = Produtos.objects.filter(codigo=OuterRef('cod_prod')).values('descricao')[:1]

    manejo_prod_queryset = ManejoProduto.objects.annotate(
        descricao=Subquery(produto_subquery)
    )

    queryset = Manejo.objects.prefetch_related(
        Prefetch('manejoproduto_set', queryset=manejo_prod_queryset)
    ).order_by("id")
    
    plantio_queryset = Plantio.objects.prefetch_related(
        Prefetch('manejo', queryset=queryset)
    ).filter(pk=pk).order_by("id")

    context = {
        "plantio_queryset": plantio_queryset,
        "plantio": plantio,
        "atividades": atividades,
        "tipos_aplicacao": tipos_aplicacao,
    }

    return render(request, "plantio/todos/plantio_view.html", context) 
   
reponse_inv_req = "Invalid request"
TZ = "Europe/London"

@csrf_exempt
def plantio_toggle_active(request, pk):
    plantio = get_object_or_404(Plantio, pk=pk)

    if request.method == "PUT" or request.method == "POST":
        plantio.data_atualizado = timezone.now().astimezone(pytz.timezone(TZ))
        plantio.ativo = not plantio.ativo
        plantio.save()
        return JsonResponse({"ativo": plantio.ativo})
    else:
        return JsonResponse({"error": reponse_inv_req})   
     
@csrf_exempt
def plantio_set_manejo(request, pk, manejo):
    plantio = get_object_or_404(Plantio, pk=pk)

    if request.method == "PUT" or request.method == "POST":
        plantio.data_atualizado = timezone.now().astimezone(pytz.timezone(TZ))
        plantio.manejo = manejo
        plantio.save()
        return JsonResponse({"manejo": plantio.manejo})
    else:
        return JsonResponse({"error": reponse_inv_req})
def prepare_data_for_excel(plantio, produtos_manejo):
    data = []
    for produto in produtos_manejo:
        base_data = [
            plantio.nome_pl,
            produto.descricao + " (" + str(produto.cod_prod) + ")",
            plantio.data_plantio + timedelta(days=produto.num_dias),
            produto.atividade.nome if produto.atividade else '',
            produto.tipo_aplicacao.nome_tipo if produto.tipo_aplicacao else '',
            "{:.2f}".format(produto.quantidade_ha).replace('.', ','),
            "{:.2f}".format(plantio.area * produto.quantidade_ha).replace('.', ',')
        ]
        
        data.append(['C'+ str(len(data)//2), *base_data, "Previsto"])
        data.append(['C'+ str(len(data)//2), *base_data, "Realizado"])
    
    return data


def get_plantio_data(pk):
    plantio = get_object_or_404(Plantio, pk=pk)
    manejo = plantio.manejo
    
    produto_subquery = Produtos.objects.filter(codigo=OuterRef('cod_prod')).values('descricao')[:1]
    
    produtos_manejo = ManejoProduto.objects.filter(manejo=manejo).order_by('num_dias').annotate(descricao=Subquery(produto_subquery))
    
    return plantio, produtos_manejo

def get_pl_excel_config():
    headers = ["N", "Plantio", "Produto", "Data de começo", "Atividade", "Tipo de Aplicação", "Quantidade/HA", "Quantidade Total", "Tipo"]
    tamanhos_colunas = {
        "N": 5,  
        "Plantio": 15,
        "Produto": 35, 
        "Data de começo": 15,
        "Atividade": 16,  
        "Tipo de Aplicação": 18,
        "Quantidade/HA": 15,
        "Quantidade Total": 15
    }
    title = "Dados Gerais do Plantio"
    
    return headers, tamanhos_colunas, title

@csrf_exempt
def pl_excel(request, pk):
    plantio, produtos_manejo = get_plantio_data(pk)
    data = prepare_data_for_excel(plantio, produtos_manejo)
    
    headers, tamanhos_colunas, title = get_pl_excel_config()
    
    return export_to_excel(data, headers, tamanhos_colunas, title, f'plantio_{pk}.xlsx')

@csrf_exempt
def pl_excel_geral(request):
    plantio_filters = request.GET.getlist("plantio_filter")
    plantios = Plantio.objects.filter(manejo__isnull=False)

    if plantio_filters and plantio_filters[0] != "":
        plantios = plantios.filter(codigo__in=plantio_filters)
    
    data = []
    for plantio in plantios:
        _, produtos_manejo = get_plantio_data(plantio.pk)
        data.extend(prepare_data_for_excel(plantio, produtos_manejo))
    
    headers, tamanhos_colunas, title = get_pl_excel_config()
    
    return export_to_excel(data, headers, tamanhos_colunas, title, 'todos_plantios.xlsx')