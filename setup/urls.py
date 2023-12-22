from django.contrib import admin
from django.urls import path
from todos.views import (
    EstufaListView,
    EstufaCreateView,
    EstufaUpdateView,
    EstufaDeleteView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", EstufaListView.as_view(), name="estufa_list"),
    path("create/", EstufaCreateView.as_view(), name="estufa_create"),
    path("update/<int:pk>", EstufaUpdateView.as_view(), name="estufa_update"),
    path("delete/<int:pk>", EstufaDeleteView.as_view(), name="estufa_delete"),
]
