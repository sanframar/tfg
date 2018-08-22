from django.shortcuts import render
from  django.http  import  HttpResponse
from django.template import loader
from django.shortcuts import render_to_response

import pandas_datareader.data as web
import datetime
import pandas as pd
import numpy as np
import os
from predicterapp.CargarDatos import obtenerDatosApi, datosYahoo
from predicterapp.PreProcesamiento import preProcesamientoDatos

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
    for aux in datosYahoo:
        datosArray.append(aux)
    template = loader.get_template('predicterapp/regresion.html')
    context = {
        'datosArray': datosArray,
    }
    return HttpResponse(template.render(context, request))


def supervisado(request):
    return render_to_response('predicterapp/supervisado.html')

def noSupervisado(request):
    return render_to_response('predicterapp/noSupervisado.html')