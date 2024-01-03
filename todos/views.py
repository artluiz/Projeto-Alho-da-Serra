from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
import json

from .models import Estufa, Atividade, Produtos, TipoIrrigador, FichaDeAplicacao

from django.shortcuts import render


def todo_home(request):
    estufas = Estufa.objects.all()
    atividades = Atividade.objects.all()
    produtos = Produtos.objects.all()
    tipos_irrigador = TipoIrrigador.objects.all()
    ran = [i for i in range(1, 11)]

    context = {
        "estufas": estufas,
        "atividades": atividades,
        "produtos": produtos,
        "tipos_irrigador": tipos_irrigador,
        "range": ran,
    }

    return render(request, "todos/home_page.html", context)


@csrf_exempt
def receber_dados(request):
    if request.method == "POST":
        print(request.body)
        # Decodifique os bytes para uma string e carregue o JSON
        dados = json.loads(request.body.decode("utf-8"))

        # Agora você pode acessar os dados como um dicionário Python
        atividade_id = dados["atividade_id"]
        estufa_id = dados["estufa_id"]
        area = dados["area"]
        irrigador_id = dados["irrigador_id"]
        dados_tabela = dados["dados_tabela"]
        data_planejada = dados["data1"]
        data_aplicada = dados["data2"]

        # Crie uma nova instância do modelo FichaDeAplicacao e salve-a no banco de dados
        ficha_aplicacao = FichaDeAplicacao(
            atividade_id=atividade_id,
            estufa_id=estufa_id,
            area=area,
            irrigador_id=irrigador_id,
            dados=dados_tabela,
            data_planejada=data_planejada,
            data_aplicada=data_aplicada,
        )
        ficha_aplicacao.save()

        return JsonResponse({"status": "success"}, safe=False)
    else:
        return JsonResponse({"status": "fail"}, safe=False)


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
    fields = ["nome_produto", "codigo", "descricao"]
    success_url = reverse_lazy("produtos_list")


class ProdutosUpdateView(UpdateView):
    model = Produtos
    fields = ["nome_produto", "codigo", "descricao"]
    success_url = reverse_lazy("produtos_list")


class ProdutosDeleteView(DeleteView):
    model = Produtos


class TipoIrrigadorListView(ListView):
    model = TipoIrrigador
