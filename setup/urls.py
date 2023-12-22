from django.contrib import admin
from django.urls import path
from todos.views import EstufaListView, EstufaCreateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", EstufaListView.as_view(), name="estufa_list"),
    path("create/", EstufaCreateView.as_view(), name="estufa_create"),
]
