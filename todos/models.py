from django.db import models


# Create your models here.
class Estufa(models.Model):
    data_criada = models.DateTimeField(
        verbose_name="Data de criação", blank=False, auto_now=False, auto_now_add=False
    )
    data_atualizado = models.DateTimeField(
        verbose_name="Data da aplicação",
        auto_now=True,
        auto_now_add=False,
    )
    nome_estufa = models.CharField(
        verbose_name="Estufa", max_length=50, null=False, blank=False
    )
    area = models.DecimalField(verbose_name="Área", decimal_places=4, max_digits=8)
    fazenda = models.CharField(
        verbose_name="fazenda", max_length=50, null=False, blank=False
    )
    ativo = models.BooleanField(default=True)


class Atividade(models.Model):
    data_criada = models.DateTimeField(
        verbose_name="Data de criação", blank=False, auto_now=False
    )
    data_atualizado = models.DateTimeField(
        verbose_name="Data da aplicação",
        auto_now=True,
        auto_now_add=False,
    )
    nome = models.CharField(
        verbose_name="Atividade", max_length=10, null=False, blank=False
    )
    # descicao = models.CharField(
    #    verbose_name="Descrição", max_length=100, null=False, blank=False
    # )
    ativo = models.BooleanField(default=True)


class Produtos(models.Model):
    data_criada = models.DateTimeField(
        verbose_name="Data de criação", blank=False, auto_now_add=False
    )
    data_atualizado = models.DateTimeField(
        verbose_name="Data da aplicação",
        auto_now=True,
        auto_now_add=False,
    )
    produto = models.CharField(
        verbose_name="Produto", max_length=50, null=False, blank=False
    )
    codigo = models.IntegerField(verbose_name="Codigo", null=False)
    descricao = models.CharField(
        verbose_name="Descrição", max_length=50, null=False, blank=False
    )
    ativo = models.BooleanField(default=True)


class TipoIrrigador(models.Model):
    nome_tipo = models.CharField(
        verbose_name="Irrigador", max_length=50, null=False, blank=False
    )
    ativo = models.BooleanField(default=True)


class FichaDeAplicacao(models.Model):
    data_criada = models.DateTimeField(
        verbose_name="Data de criação", blank=False, auto_now_add=False
    )
    data_atualizado = models.DateTimeField(
        verbose_name="Data da aplicação",
        auto_now=True,
        auto_now_add=False,
    )
    data_aplicada = models.DateField(
        verbose_name="Data real", blank=False, auto_now=False, auto_now_add=False
    )
    area = models.DecimalField(verbose_name="Área", decimal_places=4, max_digits=8)
    estufa = models.ForeignKey(Estufa, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    irrigador = models.ForeignKey(TipoIrrigador, on_delete=models.CASCADE)
    dados = models.JSONField()
    obs = models.TextField(null=True, blank=True)
    pendente = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
