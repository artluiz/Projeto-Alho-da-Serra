from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
    DetailView,
)
from django.shortcuts import redirect
import pandas as pd
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db.models import Max
import pytz
from datetime import datetime
from django.utils import timezone
import json
from todos.routers import (
    DatabaseSynchronizer,
    DatabaseDownloader,
    ModificarProdutoRouter,
)
from collections import defaultdict

from .models import Estufa, Atividade, Produtos, TipoIrrigador, FichaDeAplicacao
from .forms import ItemForm

from django.shortcuts import render


def muda_cod(request):
    # Chamar o método de classe para modificar os produtos
    response = ModificarProdutoRouter.modificar_produtos()

    # Retornar a resposta para o cliente
    return response


def sync_db_view(request):
    DatabaseDownloader.sync_db_estufa()
    DatabaseDownloader.sync_db_produto()
    DatabaseDownloader.sync_db_atividade()
    DatabaseSynchronizer.sync_db()
    return HttpResponseRedirect(reverse("ficha_list"))


def down_db_view(request):
    DatabaseDownloader.sync_db_estufa()
    DatabaseDownloader.sync_db_produto()
    DatabaseDownloader.sync_db_atividade()
    DatabaseDownloader.sync_db()
    return HttpResponseRedirect(reverse("ficha_list"))


from collections import defaultdict


class FichaRelatorioProduto(ListView):
    model = FichaDeAplicacao
    template_name = "fichadeaplicacao_relatorio_prod.html"

    def get_queryset(self):
        return FichaDeAplicacao.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estufas"] = Estufa.objects.all()
        context["atividades"] = Atividade.objects.all()
        context["tipo_irrigadores"] = TipoIrrigador.objects.all()

        # Processar os dados do queryset para estrutura desejada
        dados_estruturados = defaultdict(
            float
        )  # Dicionário padrão para armazenar previstos por produto

        queryset = self.get_queryset()
        for ficha in queryset:
            print(ficha.pk)
            for item in ficha.dados:
                if "produto" in item:
                    cod_produto = item["produto"]
                    produto = Produtos.objects.get(codigo=cod_produto)
                    item["nome_produto"] = produto.produto

        for ficha in self.get_queryset():
            if ficha.ativo:
                dados_json_lista = (
                    ficha.dados
                )  # Não é necessário usar .get() para listas
                for item in dados_json_lista:
                    if "produto" in item and "previsto" in item:
                        # Adiciona ou soma previsto ao produto na estrutura
                        if item["previsto"] != "":
                            previsto = float(item["previsto"])
                            dados_estruturados[item["produto"]] += previsto

        # Convertendo o defaultdict para um dicionário regular
        context["dados_estruturados"] = dict(dados_estruturados)

        return context


class FichaFiltro(ListView):
    model = FichaDeAplicacao
    context_object_name = "fichadeaplicacao_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estufas"] = Estufa.objects.all()
        context["atividades"] = Atividade.objects.all()
        context["tipo_irrigadores"] = TipoIrrigador.objects.all()

        # Atualizar os dados do produto
        for ficha in context["fichadeaplicacao_list"]:
            for item in ficha.dados:
                if "produto" in item:
                    cod_produto = item["produto"]
                    produto = Produtos.objects.get(codigo=cod_produto)
                    item["nome_produto"] = produto.produto
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

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

        return queryset.order_by("data_aplicada")

    def get_template_names(self):
        # Verifique a parte da URL para decidir qual template usar
        if "relatorio" in self.request.path:
            return ["fichadeaplicacao_relatorio.html"]
        return ["fichadeaplicacao_list.html"]


from collections import defaultdict


class FichaFiltroProduto(ListView):
    model = FichaDeAplicacao
    context_object_name = "fichadeaplicacao_relatorio_prod"
    template_name = "fichadeaplicacao_relatorio_prod.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estufas"] = Estufa.objects.all()
        context["atividades"] = Atividade.objects.all()
        context["tipo_irrigadores"] = TipoIrrigador.objects.all()

        queryset = self.get_queryset()

        # Estruturação dos dados
        dados_estruturados = defaultdict(float)
        for ficha in queryset:
            for item in ficha.dados:
                if "produto" in item:
                    cod_produto = item["produto"]
                    produto = Produtos.objects.get(codigo=cod_produto)
                    item["nome_produto"] = produto.produto

        for ficha in queryset:
            if ficha.ativo:
                dados_json_lista = (
                    ficha.dados
                )  # Não é necessário usar .get() para listas
                for item in dados_json_lista:
                    if "nome_produto" in item and "previsto" in item:
                        # Adiciona ou soma previsto ao produto na estrutura
                        if item["previsto"] != "":
                            previsto = float(item["previsto"])
                            dados_estruturados[item["nome_produto"]] += previsto

        # Convertendo o defaultdict para um dicionário regular
        context["dados_estruturados"] = dict(dados_estruturados)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

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


def upload_excel_file(request):
    if request.method == "POST":
        excel_file = request.FILES["inputExcel"]

        if str(excel_file).split(".")[-1] in ["xls", "xlsx"]:
            data = pd.read_excel(excel_file)
            for _, row in data.iterrows():
                produto_cod = row[
                    "Cód."
                ]  # Certifique-se de que a coluna ID exista na planilha

                # Aqui, certifique-se de que todas as colunas necessárias estejam presentes
                if (
                    pd.isna(produto_cod)
                    or pd.isna(row["Produto"])
                    or pd.isna(row["Cód."])
                    or pd.isna(row["Descrição"])
                ):
                    # Lidar com dados faltantes, por exemplo, pulando a linha ou registrando um erro
                    continue

                data_criada = timezone.now().astimezone(pytz.timezone("Europe/London"))

                produto, created = Produtos.objects.get_or_create(codigo=produto_cod)
                produto.produto = row["Produto"]
                produto.codigo = row["Cód."]
                produto.descricao = row["Descrição"]
                produto.data_criada = data_criada
                produto.data_atualizado = data_criada
                produto.save()

            return HttpResponseRedirect(reverse("produtos_list"))
        else:
            # Adicione aqui o código para lidar com o caso de o arquivo não ser um Excel
            pass
    else:
        # Adicione aqui o código para lidar com o caso de o método não ser POST
        pass


@csrf_exempt
def estufa_toggle_active(request, pk):
    obj = get_object_or_404(Estufa, pk=pk)

    if request.method == "PUT" or request.method == "POST":
        obj.data_atualizado = timezone.now().astimezone(pytz.timezone("Europe/London"))
        obj.ativo = not obj.ativo
        obj.save()
        return JsonResponse({"ativo": obj.ativo})
    else:
        return JsonResponse({"error": "Invalid request"})


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
    print("obj")
    obj = get_object_or_404(FichaDeAplicacao, pk=pk)

    if request.method == "PUT" or request.method == "POST":
        obj.data_atualizado = timezone.now().astimezone(pytz.timezone("Europe/London"))
        obj.pendente = not obj.pendente
        obj.save()
        return JsonResponse({"ativo": obj.pendente})
    else:
        return JsonResponse({"error": "Invalid request"})


@csrf_exempt
def produto_toggle_active(request, pk):
    print("obj")
    obj = get_object_or_404(Produtos, pk=pk)

    if request.method == "PUT" or request.method == "POST":
        obj.data_atualizado = timezone.now().astimezone(pytz.timezone("Europe/London"))
        obj.ativo = not obj.ativo
        obj.save()
        return JsonResponse({"ativo": obj.ativo})
    else:
        return JsonResponse({"error": "Invalid request"})


def todo_home(request):
    ficha_aplicacao_count = FichaDeAplicacao.objects.aggregate(Max("id"))["id__max"]
    if ficha_aplicacao_count is None:
        ficha_aplicacao_count = 1179
    else:
        ficha_aplicacao_count

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
    print(ficha_aplicacao)

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
        obs = dados["obs"]
        data_criada = timezone.now().astimezone(pytz.timezone("Europe/London"))

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
        print(request.body)
        # Decodifique os bytes para uma string e carregue o JSON
        dados = json.loads(request.body.decode("utf-8"))
        print(dados)
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
        print(ficha_aplicacao)
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


# views.py
from django.views.generic import ListView
from .models import FichaDeAplicacao, Estufa, Atividade, TipoIrrigador
from django.urls import reverse_lazy


class FichaListView(ListView):
    model = FichaDeAplicacao
    template_name = "fichadeaplicacao_list.html"

    def get_queryset(self):
        queryset = FichaDeAplicacao.objects.all().order_by("id")

        for ficha in queryset:
            print(ficha.pk)
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
            return ["fichadeaplicacao_relatorio.html"]
        return ["fichadeaplicacao_list.html"]


class EstufaListView(ListView):
    model = Estufa


class EstufaCreateView(CreateView):
    model = Estufa
    fields = ["nome_estufa", "area", "fazenda"]
    success_url = reverse_lazy("estufa_list")

    def form_valid(self, form):
        # Atualiza no banco de dados primário
        form.instance.save(using="default")
        # Atualiza no banco de dados secundário
        return super().form_valid(form)


class EstufaUpdateView(UpdateView):
    model = Estufa
    fields = ["nome_estufa", "area", "fazenda"]
    success_url = reverse_lazy("estufa_list")

    def form_valid(self, form):
        # Atualiza no banco de dados primário
        form.instance.save(using="default")
        # Atualiza no banco de dados secundário
        return super().form_valid(form)


class EstufaDeleteView(DeleteView):
    model = Estufa


class AtividadeListView(ListView):
    model = Atividade


class AtividadeCreateView(CreateView):
    model = Atividade
    fields = ["nome"]
    success_url = reverse_lazy("atividade_list")

    def form_valid(self, form):
        # Atualiza no banco de dados primário
        form.instance.save(using="default")
        # Atualiza no banco de dados secundário
        return super().form_valid(form)


class AtividadeUpdateView(UpdateView):
    model = Atividade
    fields = ["nome"]
    success_url = reverse_lazy("atividade_list")

    def form_valid(self, form):
        # Atualiza no banco de dados primário
        form.instance.save(using="default")
        # Atualiza no banco de dados secundário
        return super().form_valid(form)


class AtividadeDeleteView(DeleteView):
    model = Atividade


class ProdutosListView(ListView):
    model = Produtos


class ProdutosCreateView(CreateView):
    model = Produtos
    fields = ["produto", "codigo", "descricao"]
    success_url = reverse_lazy("produtos_list")

    def form_valid(self, form):
        # Atualiza no banco de dados primário
        form.instance.save(using="default")
        # Atualiza no banco de dados secundário
        return super().form_valid(form)


class ProdutosUpdateView(UpdateView):
    model = Produtos
    fields = ["produto", "codigo", "descricao"]
    success_url = reverse_lazy("produtos_list")

    def form_valid(self, form):
        # Atualiza no banco de dados primário
        form.instance.save(using="default")
        # Atualiza no banco de dados secundário
        return super().form_valid(form)


class ProdutosDeleteView(DeleteView):
    model = Produtos


class TipoIrrigadorListView(ListView):
    model = TipoIrrigador
