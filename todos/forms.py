from django import forms
from .models import Produtos


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
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


from django import forms
from .models import FichaDeAplicacao


class ItemForm(forms.ModelForm):
    class Meta:
        model = FichaDeAplicacao
        fields = ["ativo"]
