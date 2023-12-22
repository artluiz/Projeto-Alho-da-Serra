from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Estufa


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
