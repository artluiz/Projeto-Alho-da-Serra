from django.views.generic import ListView
from datetime import datetime
from django.utils import timezone
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
import pytz
from django.db.models import Max

from django.views.generic import ListView
from ..models import FichaDeAplicacao, Estufa, Atividade, Produtos, TipoIrrigador


@csrf_exempt
def ficha_toggle_active(request, pk):
    obj = get_object_or_404(FichaDeAplicacao, pk=pk)

    if request.method == "PUT" or request.method == "POST":
        obj.data_atualizado = timezone.now().astimezone(pytz.timezone("Europe/London"))
        obj.ativo = not obj.ativo
        obj.save()
        return JsonResponse({"ativo": obj.ativo})
    else:
        return JsonResponse({"error": "Invalid request"})


@csrf_exempt
def ficha_toggle_pendente(request, pk):
    obj = get_object_or_404(FichaDeAplicacao, pk=pk)

    if request.method == "PUT" or request.method == "POST":
        obj.data_atualizado = timezone.now().astimezone(pytz.timezone("Europe/London"))
        obj.pendente = not obj.pendente
        obj.save()
        return JsonResponse({"ativo": obj.pendente})
    else:
        return JsonResponse({"error": "Invalid request"})


def todo_home(request):
    ficha_aplicacao_count = FichaDeAplicacao.objects.aggregate(Max("id"))["id__max"]
    if ficha_aplicacao_count is None:
        ficha_aplicacao_count = 1179

    estufas = Estufa.objects.all()
    atividades = Atividade.objects.all()
    produtos = Produtos.objects.all().order_by("descricao")
    tipos_irrigador = TipoIrrigador.objects.all()
    ran = [i for i in range(1, 11)]

    context = {
        "fcc": ficha_aplicacao_count + 1,
        "estufas": estufas,
        "atividades": atividades,
        "produtos": produtos,
        "tipos_irrigador": tipos_irrigador,
        "range": ran,
    }

    return render(request, "todos/home_page.html", context)


def todo_repetir(request, pk):
    ficha_aplicacao = get_object_or_404(FichaDeAplicacao, pk=pk)
    estufas = Estufa.objects.all()
    atividades = Atividade.objects.all()
    produtos = Produtos.objects.all().order_by("descricao")
    tipos_irrigador = TipoIrrigador.objects.all()
    ran = [i for i in range(1, 11)]
    pk_view = ficha_aplicacao.pk + 1

    for item in ficha_aplicacao.dados:
        if "produto" in item:
            cod_produto = item["produto"]
            produto = Produtos.objects.get(codigo=cod_produto)
            item["nome_produto"] = produto.produto

    if len(ficha_aplicacao.dados) < 10:
        ficha_aplicacao.dados += [{}] * (10 - len(ficha_aplicacao.dados))

    context = {
        "ficha": ficha_aplicacao,
        "estufas": estufas,
        "atividades": atividades,
        "produtos": produtos,
        "tipos_irrigador": tipos_irrigador,
        "range": ran,
        "pk_view": pk_view,
    }

    return render(request, "todos/home_repetir.html", context)


def todo_update(request, pk):
    ficha_aplicacao = get_object_or_404(FichaDeAplicacao, pk=pk)
    estufas = Estufa.objects.all()
    atividades = Atividade.objects.all()
    produtos = Produtos.objects.all().order_by("descricao")
    tipos_irrigador = TipoIrrigador.objects.all()
    ran = [i for i in range(1, 11)]

    for item in ficha_aplicacao.dados:
        if "produto" in item:
            cod_produto = item["produto"]
            produto = Produtos.objects.get(codigo=cod_produto)
            item["nome_produto"] = produto.produto

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


@csrf_exempt
def receber_dados(request):
    if request.method == "POST" or request.method == "PUT":
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
        obs = dados["obs"]
        data_criada = timezone.now()

        # data_planejada = datetime.strptime(dados["data1"], "%Y-%m-%d")
        data_aplicada = datetime.strptime(dados["data1"], "%Y-%m-%d")

        data_aplicada = pytz.timezone("Europe/London").localize(data_aplicada)

        # Crie uma nova instância do modelo FichaDeAplicacao e salve-a no banco de dados
        ficha_aplicacao = FichaDeAplicacao(
            data_atualizado=data_criada,
            data_criada=data_criada,
            atividade=atividade_id,
            estufa=estufa_id,
            area=area,
            irrigador=irrigador_id,
            dados=dados_tabela,
            # data_planejada=data_planejada,
            data_aplicada=data_aplicada,
            obs=obs,
        )
        ficha_aplicacao.save()

        return JsonResponse({"status": "success"}, safe=False)
    else:
        return JsonResponse({"status": "fail"}, safe=False)


@csrf_exempt
def atualizar_dados(request):
    if request.method == "PUT":
        # Decodifique os bytes para uma string e carregue o JSON
        dados = json.loads(request.body.decode("utf-8"))
        # Obtenha a ficha existente pelo id
        ficha_aplicacao = get_object_or_404(FichaDeAplicacao, pk=dados["ficha_pk"])

        # Atualize os campos desejados
        ficha_aplicacao.atividade = Atividade.objects.get(pk=(dados["atividade_id"]))
        ficha_aplicacao.estufa = Estufa.objects.get(pk=(dados["estufa_id"]))
        # ficha_aplicacao.area = dados["area"].replace(",", ".")
        ficha_aplicacao.area = dados["area"]
        ficha_aplicacao.irrigador = TipoIrrigador.objects.get(
            pk=(dados["irrigador_id"])
        )
        ficha_aplicacao.dados = dados["dados_tabela"]
        # ficha_aplicacao.data_planejada = datetime.strptime(dados["data1"], "%Y-%m-%d")
        ficha_aplicacao.data_aplicada = datetime.strptime(dados["data"], "%Y-%m-%d")

        # ficha_aplicacao.data_planejada = pytz.timezone("Europe/London").localize(
        #    ficha_aplicacao.data_planejada
        # )
        ficha_aplicacao.data_aplicada = pytz.timezone("Europe/London").localize(
            ficha_aplicacao.data_aplicada
        )
        ficha_aplicacao.data_atualizado = timezone.now().astimezone(
            pytz.timezone("Europe/London")
        )

        # Salve a instância para atualizar o banco de dados
        ficha_aplicacao.save()

        return JsonResponse({"status": "success"}, safe=False)
    else:
        return JsonResponse({"status": "fail"}, safe=False)


def ImprimirFicha(request, pk):
    ficha_aplicacao = get_object_or_404(FichaDeAplicacao, pk=pk)
    estufas = Estufa.objects.all()
    atividades = Atividade.objects.all()
    produtos = Produtos.objects.all()
    tipos_irrigador = TipoIrrigador.objects.all()
    ran = [i for i in range(1, 11)]

    for item in ficha_aplicacao.dados:
        if "produto" in item:
            cod_produto = item["produto"]
            produto = Produtos.objects.get(codigo=cod_produto)
            item["nome_produto"] = produto.produto

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

    return render(request, "todos/fichadeaplicacao_detail.html", context)


def FichaView(request, pk):
    ficha_aplicacao = get_object_or_404(FichaDeAplicacao, pk=pk)
    estufas = Estufa.objects.all()
    atividades = Atividade.objects.all()
    produtos = Produtos.objects.all()
    tipos_irrigador = TipoIrrigador.objects.all()
    ran = [i for i in range(1, 11)]

    for item in ficha_aplicacao.dados:
        if "produto" in item:
            cod_produto = item["produto"]
            produto = Produtos.objects.get(codigo=cod_produto)
            item["nome_produto"] = produto.produto

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

    return render(request, "todos/ficha_view.html", context)


class FichaListView(ListView):
    model = FichaDeAplicacao
    template_name = "fichadeaplicacao_list.html"

    def get_queryset(self):
        queryset = FichaDeAplicacao.objects.all().order_by("id")

        for ficha in queryset:
            for item in ficha.dados:
                if "produto" in item:
                    cod_produto = item["produto"]
                    produto = Produtos.objects.get(codigo=cod_produto)

                    item["nome_produto"] = produto.produto

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["estufas"] = Estufa.objects.all()
        context["atividades"] = Atividade.objects.all()
        context["tipo_irrigadores"] = TipoIrrigador.objects.all()

        return context

    def get_template_names(self):
        if "relatorio" in self.request.path:
            return ["fichadeaplicacao/todos/fichadeaplicacao_relatorio.html"]
        return ["fichadeaplicacao/todos/fichadeaplicacao_list.html"]


class FichaFilter:
    def __init__(self, request):
        self.request = request

    def apply_filters(self, queryset):
        atividade_filter = self.request.GET.get("atividade_filter")
        estufa_filter = self.request.GET.get("estufa_filter")
        status_filter = self.request.GET.get("status_filter")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(data_criada__range=(start_date, end_date))
        else:
            if start_date:
                queryset = queryset.filter(data_criada__date=start_date)

        if atividade_filter:
            queryset = queryset.filter(atividade__id=atividade_filter)

        if estufa_filter:
            queryset = queryset.filter(estufa__id=estufa_filter)

        if status_filter is not None:
            if status_filter == "true":
                queryset = queryset.filter(pendente=False)
            elif status_filter == "false":
                queryset = queryset.filter(pendente=True)

        return queryset


class FichaBaseView(ListView):
    model = FichaDeAplicacao
    context_object_name = "fichadeaplicacao_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estufas"] = Estufa.objects.all()
        context["atividades"] = Atividade.objects.all()
        context["tipo_irrigadores"] = TipoIrrigador.objects.all()

        for ficha in context[self.context_object_name]:
            for item in ficha.dados:
                if "produto" in item:
                    cod_produto = item["produto"]
                    produto = Produtos.objects.get(codigo=cod_produto)
                    item["nome_produto"] = produto.produto
        return context

    def get_queryset(self):
        return (
            FichaFilter(self.request)
            .apply_filters(super().get_queryset())
            .order_by("data_aplicada")
        )

    def estruturar_dados(self, queryset):
        dados_estruturados = defaultdict(float)
        for ficha in queryset:
            print(ficha)
            if ficha.ativo:
                for item in ficha.dados:
                    if "nome_produto" in item and "previsto" in item:
                        if item["previsto"] != "":
                            previsto = float(item["previsto"])
                            dados_estruturados[item["nome_produto"]] += previsto
        return dict(dados_estruturados)


class FichaRelatorioProduto(FichaBaseView):
    template_name = "fichadeaplicacao/todos/fichadeaplicacao_relatorio_prod.html"

    def get_queryset(self):
        return FichaDeAplicacao.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["dados_estruturados"] = self.estruturar_dados(queryset)
        return context


class FichaFiltro(FichaBaseView):

    def get_template_names(self):
        if "relatorio" in self.request.path:
            return ["fichadeaplicacao/todos/fichadeaplicacao_relatorio.html"]
        return ["fichadeaplicacao/todos/fichadeaplicacao_list.html"]


class FichaFiltroProduto(FichaBaseView):
    context_object_name = "fichadeaplicacao/todos/fichadeaplicacao_relatorio_prod"
    template_name = "fichadeaplicacao/todos/fichadeaplicacao_relatorio_prod.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["dados_estruturados"] = self.estruturar_dados(queryset)
        return context
