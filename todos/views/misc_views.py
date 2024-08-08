from django.views.generic import (
    ListView,
)
import pandas as pd
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
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

from ..models import Estufa, Atividade, Produtos, TipoIrrigador, FichaDeAplicacao
from ..forms import ItemForm


def muda_cod(request):
    response = ModificarProdutoRouter.modificar_produtos()

    return response


def sync_db_view(request):
    DatabaseSynchronizer.sync_db_atividade()
    DatabaseSynchronizer.sync_db_estufa()
    DatabaseSynchronizer.sync_db_produto()
    DatabaseSynchronizer.sync_db()
    return HttpResponseRedirect(reverse("ficha_list"))


def down_db_view(request):
    DatabaseDownloader.sync_db_atividade()
    DatabaseDownloader.sync_db_estufa()
    DatabaseDownloader.sync_db_produto()
    DatabaseDownloader.sync_db()
    return HttpResponseRedirect(reverse("ficha_list"))


from collections import defaultdict


def upload_excel_file(request):
    if request.method == "POST":
        excel_file = request.FILES["inputExcel"]

        if str(excel_file).split(".")[-1] in ["xls", "xlsx"]:
            data = pd.read_excel(excel_file)
            for _, row in data.iterrows():
                produto_cod = row[
                    "Cód."
                ]  # Certifique-se de que a coluna ID exista na planilha

                if (
                    pd.isna(produto_cod)
                    or pd.isna(row["Produto"])
                    or pd.isna(row["Cód."])
                    or pd.isna(row["Descrição"])
                ):
                    # Lidar com dados faltantes, por exemplo, pulando a linha ou registrando um erro
                    continue

                data_criada = datetime.now()

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
