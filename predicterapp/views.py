from django.shortcuts import render
from  django.http  import  HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
# -*- coding: utf-8 -*-
# Create your views here.

def  index ( request ): 
    return render_to_response('predicterapp/index.html')

def datos(request):
    datosBBDD = ["Santander", "BBVA", "Unicaja", "BCE", "Caixa"]
    template = loader.get_template('predicterapp/datos.html')
    context = {
        'datosBBDD': datosBBDD,
    }
    return HttpResponse(template.render(context, request))

def supervisado(request):
    return render_to_response('predicterapp/supervisado.html')

def noSupervisado(request):
    return render_to_response('predicterapp/noSupervisado.html')