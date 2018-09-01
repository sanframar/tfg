from django import forms

class FormularioRegresion(forms.Form):
    diasAPredecir = forms.IntegerField(label='Dias a predecir', max_value=100)