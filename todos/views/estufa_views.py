from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from datetime import datetime
from django.utils import timezone

import pytz
from ..models import Estufa


class EstufaListView(ListView):
    model = Estufa


class EstufaCreateView(CreateView):
    model = Estufa
    fields = ["nome_estufa", "area", "fazenda"]
    success_url = reverse_lazy("estufa_list")

    def form_valid(self, form):
        form.instance.data_criada = datetime.now()
        form.instance.save(using="default")
        return super().form_valid(form)


class EstufaUpdateView(UpdateView):
    model = Estufa
    fields = ["nome_estufa", "area", "fazenda"]
    success_url = reverse_lazy("estufa_list")

    def form_valid(self, form):
        form.instance.save(using="default")
        return super().form_valid(form)


class EstufaDeleteView(DeleteView):
    model = Estufa


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
