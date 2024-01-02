from django import forms


class area_form(forms.Form):
    area = forms.FloatField(label="Área", required=True)
