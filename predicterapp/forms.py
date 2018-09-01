from django import forms
from predicterapp.CargarDatos import datosYahooTupla, datosYahoo

class FormularioRegresion(forms.Form):
    diasAPredecir = forms.IntegerField(label='Dias a predecir', max_value=100)
    select = forms.ChoiceField(choices=datosYahooTupla)