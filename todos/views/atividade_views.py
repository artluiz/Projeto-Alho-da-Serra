from datetime import datetime
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now

from ..models import Atividade


class AtividadeListView(ListView):
    model = Atividade


class AtividadeCreateView(CreateView):
    model = Atividade
    fields = ["nome"]
    success_url = reverse_lazy("atividade_list")

    def form_valid(self, form):
        form.instance.save(using="default")
        return super().form_valid(form)


class AtividadeUpdateView(UpdateView):
    model = Atividade
    fields = ["nome"]
    success_url = reverse_lazy("atividade_list")

    def form_valid(self, form):
        form.instance.data_criada = datetime.now()
        form.instance.save(using="default")
        return super().form_valid(form)


class AtividadeDeleteView(DeleteView):
    model = Atividade
