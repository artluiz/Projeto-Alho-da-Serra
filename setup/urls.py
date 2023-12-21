from django.contrib import admin
from django.urls import path
from todos.views import estufa

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", estufa),
]
