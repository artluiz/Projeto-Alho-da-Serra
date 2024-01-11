from django import forms
from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["produto", "codigo", "descricao"]
        widgets = {
            "produto": forms.Select(
                attrs={
                    "class": "select2",
                    "data-placeholder": "Selecione um produto...",
                }
            ),
        }


class area_form(forms.Form):
    area = forms.FloatField(label="Área", required=False)
