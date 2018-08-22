'''
Created on 10 jul. 2018

@author: Santiago
'''
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # URL: Pagina principal
    path('', views.index, name='index'),
    # URL: Datos almacenados
    path('datos', views.datos, name='datos'),
    # URL: Pre procesamiento
    path('preProcesamiento', views.preProcesamiento, name='preProcesamiento'),
    # URL: Regresion
    path('regresion', views.regresion, name='regresion'),
    # URL: Aprendizaje Supervisado
    path('supervisado', views.supervisado, name='supervisado'),
    # URL: Aprendizaje No Supervisado
    path('noSupervisado', views.noSupervisado, name='noSupervisado'),
]
