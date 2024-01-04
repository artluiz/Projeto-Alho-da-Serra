from django.contrib import admin
from django.urls import path
from todos.views import (
    todo_home,
    todo_update,
    todo_edit,
    receber_dados,
    FichaListView,
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
    path("update/<int:pk>", todo_update, name="ficha_update"),
    path("edit/<int:pk>", todo_edit, name="ficha_edit"),
    path("receber_dados/", receber_dados, name="receber_dados"),
    path("ficha", FichaListView.as_view(), name="ficha_list"),
    path("estufa", EstufaListView.as_view(), name="estufa_list"),
    path("estufa/create/", EstufaCreateView.as_view(), name="estufa_create"),
    path("estufa/update/<int:pk>", EstufaUpdateView.as_view(), name="estufa_update"),
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
        "produtos/delete/<int:pk>", ProdutosDeleteView.as_view(), name="produtos_delete"
    ),
    path("irrigadores", TipoIrrigadorListView.as_view(), name="irrigador_list"),
]
