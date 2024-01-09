from django.contrib import admin
from django.urls import path
from todos.views import (
    todo_home,
    todo_update,
    todo_edit,
    receber_dados,
    atualizar_dados,
    ficha_toggle_pendente,
    ficha_toggle_active,
    produto_toggle_active,
    estufa_toggle_active,
    FichaFiltro,
    FichaListView,
    ImprimirFicha,
    EstufaListView,
    EstufaCreateView,
    EstufaUpdateView,
    EstufaDeleteView,
    AtividadeListView,
    AtividadeCreateView,
    AtividadeUpdateView,
    AtividadeDeleteView,
    ProdutosCreateView,
    ProdutosListView,
    ProdutosUpdateView,
    ProdutosDeleteView,
    TipoIrrigadorListView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", todo_home, name="home_page"),
    path("ficha/toggle/<int:pk>", ficha_toggle_active, name="ficha_toggle_active"),
    path(
        "ficha/toggle_p/<int:pk>", ficha_toggle_pendente, name="ficha_toggle_pendente"
    ),
    path("ficha/imprimir/<int:pk>/", ImprimirFicha, name="imprimir_ficha"),
    path("update/<int:pk>", todo_update, name="ficha_update"),
    path("edit/<int:pk>", todo_edit, name="ficha_edit"),
    path("receber_dados/", receber_dados, name="receber_dados"),
    path("atualizar_dados/", atualizar_dados, name="atualizar_dados"),
    path("ficha", FichaListView.as_view(), name="ficha_list"),
    path("ficha_filtro/", FichaFiltro.as_view(), name="ficha_filtro"),
    path("estufa", EstufaListView.as_view(), name="estufa_list"),
    path("estufa/create/", EstufaCreateView.as_view(), name="estufa_create"),
    path("estufa/update/<int:pk>", EstufaUpdateView.as_view(), name="estufa_update"),
    path("estufa/toggle/<int:pk>", estufa_toggle_active, name="estufa_toggle_active"),
    path("estufa/delete/<int:pk>", EstufaDeleteView.as_view(), name="estufa_delete"),
    path("atividade", AtividadeListView.as_view(), name="atividade_list"),
    path("atividade/create/", AtividadeCreateView.as_view(), name="atividade_create"),
    path(
        "atividade/update/<int:pk>",
        AtividadeUpdateView.as_view(),
        name="atividade_update",
    ),
    path(
        "atividade/delete/<int:pk>",
        AtividadeDeleteView.as_view(),
        name="atividade_delete",
    ),
    path("produto", ProdutosListView.as_view(), name="produtos_list"),
    path("produto/create/", ProdutosCreateView.as_view(), name="produtos_create"),
    path(
        "produtos/update/<int:pk>",
        ProdutosUpdateView.as_view(),
        name="produtos_update",
    ),
    path(
        "produto/toggle/<int:pk>", produto_toggle_active, name="produto_toggle_active"
    ),
    path(
        "produtos/delete/<int:pk>", ProdutosDeleteView.as_view(), name="produtos_delete"
    ),
    path("irrigadores", TipoIrrigadorListView.as_view(), name="irrigador_list"),
]
