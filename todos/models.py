from django.db import models


# Create your models here.
class Estufa(models.Model):
    nome_estufa = models.CharField(max_length=50, null=False, blank=False)
    area = models.DecimalField(decimal_places=4, max_digits=8)
    Fazenda = models.CharField(max_length=50, null=False, blank=False)


class Atividade(models.Model):
    nome = models.CharField(max_length=10, null=False, blank=False)


class Produtos(models.Model):
    nome_produto = models.CharField(max_length=30, null=False, blank=False)
    codigo = models.IntegerField(null=False)
    descricao = models.CharField(max_length=100, null=False, blank=False)


class TipoIrrigador(models.Model):
    nome_tipo = models.CharField(max_length=50, null=False, blank=False)


class FichaDeAplicacao(models.Model):
    data_criada = models.DateTimeField(blank=False, auto_now=False, auto_now_add=True)
    data_planejada = models.DateTimeField(
        blank=False, auto_now=False, auto_now_add=False
    )
    data_aplicada = models.DateTimeField(
        blank=False, auto_now=False, auto_now_add=False
    )
    atividade_id = models.PositiveIntegerField(null=False)
    estufa_id = models.PositiveIntegerField(null=False)
    produto_id = models.PositiveIntegerField(null=False)
    irrigador_id = models.PositiveIntegerField(null=False)
