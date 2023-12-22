from django.db import models


# Create your models here.
class Estufa(models.Model):
    nome_estufa = models.CharField(
        verbose_name="Estufa", max_length=50, null=False, blank=False
    )
    area = models.DecimalField(verbose_name="Área", decimal_places=4, max_digits=8)
    Fazenda = models.CharField(
        verbose_name="Fazenda", max_length=50, null=False, blank=False
    )


class Atividade(models.Model):
    nome = models.CharField(
        verbose_name="Atividade", max_length=10, null=False, blank=False
    )


class Produtos(models.Model):
    nome_produto = models.CharField(
        verbose_name="Produto", max_length=30, null=False, blank=False
    )
    codigo = models.IntegerField(verbose_name="Codigo", null=False)
    descricao = models.CharField(
        verbose_name="Descrição", max_length=100, null=False, blank=False
    )


class TipoIrrigador(models.Model):
    nome_tipo = models.CharField(
        verbose_name="Irrigador", max_length=50, null=False, blank=False
    )


class FichaDeAplicacao(models.Model):
    data_criada = models.DateTimeField(
        verbose_name="Data de criação", blank=False, auto_now=False, auto_now_add=True
    )
    data_planejada = models.DateTimeField(
        verbose_name="Data da aplicação",
        blank=False,
        auto_now=False,
        auto_now_add=False,
    )
    data_aplicada = models.DateTimeField(
        verbose_name="Data real", blank=False, auto_now=False, auto_now_add=False
    )
    atividade_id = models.PositiveIntegerField(
        verbose_name="Atividade associada", null=False
    )
    estufa_id = models.PositiveIntegerField(verbose_name="Estufa associada", null=False)
    produto_id = models.PositiveIntegerField(
        verbose_name="Produto associado", null=False
    )
    irrigador_id = models.PositiveIntegerField(
        verbose_name="Irrigador associado", null=False
    )
