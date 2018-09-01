from django.shortcuts import render
from  django.http  import  HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

import pandas_datareader.data as web
import datetime
import pandas as pd
import numpy as np
import os
from predicterapp.CargarDatos import obtenerDatosApi, datosYahoo
from predicterapp.PreProcesamiento import preProcesamientoDatos
from .forms import FormularioRegresion

# -*- coding: utf-8 -*-
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def  index ( request ): 
    return render_to_response('predicterapp/index.html')

def datos(request):
    obtenerDatosApi()
    BBDD = []
    try:
        for x in datosYahoo:
            datos = pd.read_pickle(BASE_DIR + '\predicterapp\static\predicterapp\myDates\dataframe\\' + x + '.infer')
        
            fechaInicio = datos.head(1).reset_index()['Date'][0]
            fechaFin = datos.tail(1).reset_index()['Date'][0]
            tamDatos = datos.size
            tupla = [x, fechaInicio, fechaFin, tamDatos]
            BBDD.append(tupla)
            print(BBDD)
    except:
        fechaInicio = "Sin fecha inicio"
        fechaFin = "Sin fecha fin"
        tamDatos = 0
    
    template = loader.get_template('predicterapp/datos.html')
    context = {
        'BBDD': BBDD,
    }
    return HttpResponse(template.render(context, request))

def preProcesamiento(request):
    preProcesamientoDatos()
    BBDD = []
    try:
        for x in datosYahoo:
            datosArray = np.load(BASE_DIR + '\\predicterapp\\static\\predicterapp\\myDates\\narray\\' + x + '.npy')
            datosDataframe = pd.read_pickle(BASE_DIR + '\predicterapp\static\predicterapp\myDates\dataframe\\' + x + '.infer')
        
            #Estadisticas del conjunto de datos pre procesados
            valorMinimoArray = datosArray.min()
            valorMaximoArray = datosArray.max()
            valorMedioArray = np.mean(datosArray)
            valoresNaNArray = np.isnan(datosArray).sum()
            
            #Estadisticas del conjunto de datos sin el pre procesado
            valorMinimoDataframe = datosDataframe.loc[datosDataframe['Close'].idxmin()][0]
            valorMaximoDataframe = datosDataframe.loc[datosDataframe['Close'].idxmax()][0]
            valorMedioDataframe = datosDataframe['Close'].median()
            valoresNaNDataframe = datosDataframe['Close'].isnull().sum()
            
            tupla = [x, valoresNaNArray, valorMinimoArray, valorMaximoArray, valorMedioArray, valorMinimoDataframe, valorMaximoDataframe, valorMedioDataframe, valoresNaNDataframe]
            BBDD.append(tupla)
    except:
        print("Error al mostrar los datos del pre-procesamiento")
    
    template = loader.get_template('predicterapp/preProcesamiento.html')
    context = {
        'BBDD': BBDD,
    }
    return HttpResponse(template.render(context, request))

def regresion ( request ): 
    datosArray = []
    form = FormularioRegresion()
    for aux in datosYahoo:
        datosArray.append(aux)
    template = loader.get_template('predicterapp/regresion.html')
    context = {
        'datosArray': datosArray,
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def formularioParaRegresion(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = FormularioRegresion(request.GET)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            #return HttpResponseRedirect(resultadoRegresion(form))
            return resultadoRegresion(form)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormularioRegresion()
        return render(request, 'predicterapp/regresion.html', {'form': form})
    #return render(request, 'predicterapp/regresion.html', {'form': form})

def resultadoRegresion(form):
    numeroDias = form.data['diasAPredecir']
    print(type(numeroDias))
            
    template = loader.get_template('predicterapp/resultadoRegresion.html')
    context = {
        'numeroDias': numeroDias,
    }
    return HttpResponse(template.render(context))

def supervisado(request):
    return render_to_response('predicterapp/supervisado.html')

def noSupervisado(request):
    return render_to_response('predicterapp/noSupervisado.html')