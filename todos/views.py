from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models import Estufa


class EstufaListView(ListView):
    model = Estufa


class EstufaCreateView(CreateView):
    model = Estufa
    fields = ["nome_estufa", "area", "Fazenda"]
    success_url = reverse_lazy("estufa_list")


#              href="{% url 'estufa_delete' pk=estufa.pk %}"

# href="{% url 'estufa_update' pk=estufa.pk %}"
