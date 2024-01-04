from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Max
import pytz
from datetime import datetime
from django.utils import timezone
import json

from .models import Estufa, Atividade, Produtos, TipoIrrigador, FichaDeAplicacao

from django.shortcuts import render


def todo_home(request):
    ficha_aplicacao_count = FichaDeAplicacao.objects.aggregate(Max("id"))["id__max"] + 1
    estufas = Estufa.objects.all()
    atividades = Atividade.objects.all()
    produtos = Produtos.objects.all()
    tipos_irrigador = TipoIrrigador.objects.all()
    ran = [i for i in range(1, 11)]

    context = {
        "fcc": ficha_aplicacao_count,
        "estufas": estufas,
        "atividades": atividades,
        "produtos": produtos,
        "tipos_irrigador": tipos_irrigador,
        "range": ran,
    }

    return render(request, "todos/home_page.html", context)


def todo_update(request, pk):
    ficha_aplicacao = get_object_or_404(FichaDeAplicacao, pk=pk)
    estufas = Estufa.objects.all()
    atividades = Atividade.objects.all()
    produtos = Produtos.objects.all()
    tipos_irrigador = TipoIrrigador.objects.all()
    ran = [i for i in range(1, 11)]

    if len(ficha_aplicacao.dados) < 10:
        ficha_aplicacao.dados += [{}] * (10 - len(ficha_aplicacao.dados))

    context = {
        "ficha": ficha_aplicacao,
        "estufas": estufas,
        "atividades": atividades,
        "produtos": produtos,
        "tipos_irrigador": tipos_irrigador,
        "range": ran,
    }

    return render(request, "todos/home_update.html", context)


def todo_edit(request, pk):
    ficha_aplicacao = get_object_or_404(FichaDeAplicacao, pk=pk)
    estufas = Estufa.objects.all()
    atividades = Atividade.objects.all()
    produtos = Produtos.objects.all()
    tipos_irrigador = TipoIrrigador.objects.all()
    ran = [i for i in range(1, 11)]

    if len(ficha_aplicacao.dados) < 10:
        ficha_aplicacao.dados += [{}] * (10 - len(ficha_aplicacao.dados))

    context = {
        "ficha": ficha_aplicacao,
        "estufas": estufas,
        "atividades": atividades,
        "produtos": produtos,
        "tipos_irrigador": tipos_irrigador,
        "range": ran,
    }

    return render(request, "todos/home_edit.html", context)


@csrf_exempt
def receber_dados(request):
    if request.method == "POST" or request.method == "PUT":
        print(request.body)
        # Decodifique os bytes para uma string e carregue o JSON
        dados = json.loads(request.body.decode("utf-8"))

        # Agora você pode acessar os dados como um dicionário Python
        if request.method == "PUT":
            ficha_aplicacao = get_object_or_404(
                FichaDeAplicacao, pk=Atividade.objects.get(pk=(dados["ficha_pk"]))
            )
        atividade_id = Atividade.objects.get(pk=(dados["atividade_id"]))
        estufa_id = Estufa.objects.get(pk=(dados["estufa_id"]))
        area = dados["area"]
        irrigador_id = TipoIrrigador.objects.get(pk=(dados["irrigador_id"]))
        dados_tabela = dados["dados_tabela"]
        data_criada = timezone.now().astimezone(pytz.timezone("America/Sao_Paulo"))
        data_planejada = datetime.strptime(dados["data1"], "%Y-%m-%d")
        data_aplicada = datetime.strptime(dados["data2"], "%Y-%m-%d")

        data_planejada = pytz.timezone("America/Sao_Paulo").localize(data_planejada)
        data_aplicada = pytz.timezone("America/Sao_Paulo").localize(data_aplicada)

        # Crie uma nova instância do modelo FichaDeAplicacao e salve-a no banco de dados
        ficha_aplicacao = FichaDeAplicacao(
            data_criada=data_criada,
            atividade=atividade_id,
            estufa=estufa_id,
            area=area,
            irrigador=irrigador_id,
            dados=dados_tabela,
            data_planejada=data_planejada,
            data_aplicada=data_aplicada,
        )
        ficha_aplicacao.save()

        return JsonResponse({"status": "success"}, safe=False)
    else:
        return JsonResponse({"status": "fail"}, safe=False)


class FichaListView(ListView):
    model = FichaDeAplicacao

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estufas"] = Estufa.objects.all()
        context["atividades"] = Atividade.objects.all()
        context["tipo_irrigadores"] = TipoIrrigador.objects.all()
        return context

    success_url = reverse_lazy("ficha_list")


class EstufaListView(ListView):
    model = Estufa


class EstufaCreateView(CreateView):
    model = Estufa
    fields = ["nome_estufa", "area", "Fazenda"]
    success_url = reverse_lazy("estufa_list")


class EstufaUpdateView(UpdateView):
    model = Estufa
    fields = ["nome_estufa", "area", "Fazenda"]
    success_url = reverse_lazy("estufa_list")


class EstufaDeleteView(DeleteView):
    model = Estufa


class AtividadeListView(ListView):
    model = Atividade


class AtividadeCreateView(CreateView):
    model = Atividade
    fields = ["nome"]
    success_url = reverse_lazy("atividade_list")


class AtividadeUpdateView(UpdateView):
    model = Atividade
    fields = ["nome"]
    success_url = reverse_lazy("atividade_list")


class AtividadeDeleteView(DeleteView):
    model = Atividade


class ProdutosListView(ListView):
    model = Produtos


class ProdutosCreateView(CreateView):
    model = Produtos
    fields = ["produto", "codigo", "descricao"]
    success_url = reverse_lazy("produtos_list")


class ProdutosUpdateView(UpdateView):
    model = Produtos
    fields = ["produto", "codigo", "descricao"]
    success_url = reverse_lazy("produtos_list")


class ProdutosDeleteView(DeleteView):
    model = Produtos


class TipoIrrigadorListView(ListView):
    model = TipoIrrigador
