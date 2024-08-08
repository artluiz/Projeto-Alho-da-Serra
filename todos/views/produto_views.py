from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
import pytz

from ..models import Produtos
from datetime import datetime
from django.utils import timezone

reponse_inv_req = "Invalid request"
TZ = "Europe/London"


class ProdutosListView(ListView):
    model = Produtos


class ProdutosCreateView(CreateView):
    model = Produtos
    fields = ["produto", "codigo", "descricao"]
    success_url = reverse_lazy("produtos_list")

    def form_valid(self, form):
        form.instance.data_criada = datetime.now()
        form.instance.save(using="default")
        return super().form_valid(form)


class ProdutosUpdateView(UpdateView):
    model = Produtos
    fields = ["produto", "codigo", "descricao"]
    success_url = reverse_lazy("produtos_list")

    def form_valid(self, form):
        form.instance.save(using="default")
        return super().form_valid(form)


class ProdutosDeleteView(DeleteView):
    model = Produtos
    success_url = reverse_lazy("produtos_list")


@csrf_exempt
def produto_toggle_active(request, pk):
    obj = get_object_or_404(Produtos, pk=pk)

    if request.method == "PUT" or request.method == "POST":
        obj.data_atualizado = timezone.now().astimezone(pytz.timezone(TZ))
        obj.ativo = not obj.ativo
        obj.save()
        return JsonResponse({"ativo": obj.ativo})
    else:
        return JsonResponse({"error": reponse_inv_req})
