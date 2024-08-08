from django.views.generic import ListView


from todos.models import TipoIrrigador


class TipoIrrigadorListView(ListView):
    model = TipoIrrigador
