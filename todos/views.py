from django.shortcuts import render
from .models import Estufa

def home(request):
    return render(request, "todos/home.html")

def estufa(request):
    estufas = Estufa.objects.all()
    return render(request, "todos/estufa_list.html", {"estufas": estufas})
