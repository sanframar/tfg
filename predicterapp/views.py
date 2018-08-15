from django.shortcuts import render
from  django.http  import  HttpResponse
from django.template import loader
from django.shortcuts import render_to_response

import pandas_datareader.data as web
import datetime
import pandas as pd
import os
from predicterapp.CargarDatos import obtenerDatosApi, datosYahoo

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
            datos = pd.read_pickle(BASE_DIR + '\predicterapp\static\predicterapp\myDates\\' + x + '.infer')
        
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
    return render_to_response('predicterapp/preProcesamiento.html')

def supervisado(request):
    return render_to_response('predicterapp/supervisado.html')

def noSupervisado(request):
    return render_to_response('predicterapp/noSupervisado.html')