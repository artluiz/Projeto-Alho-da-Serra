from django.db import models

# Create your models here.
class Estufa(models.Model):
    nome_estufa = models.CharField(max_length=50, null =False, blank=False)
    area = models.DecimalField(max_digits=8, decimal_places=4)
    Fazenda = models.CharField(max_length=50, null =False, blank=False)

#Estufa	Área	Fazenda