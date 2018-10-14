from django import forms
from predicterapp.CargarDatos import datosYahooTupla, datosYahoo
import datetime

class FormularioRegresion(forms.Form):
    diasAPredecir = forms.IntegerField(label='Dias a predecir', max_value=100)
    select = forms.ChoiceField(choices=datosYahooTupla)
    fechaIniTrain = forms.DateField(label='Fecha de inicio (Training)', initial = 'aaaa-mm-dd')
    fechaFinTrain = forms.DateField(label='Fecha de fin (Training)', initial = 'aaaa-mm-dd')
    fechaIniTest = forms.DateField(label='Fecha de inicio (Test)', initial = 'aaaa-mm-dd')
    fechaFinTest = forms.DateField(label='Fecha de fin (Test)', initial = 'aaaa-mm-dd')