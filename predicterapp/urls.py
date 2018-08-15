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
    # URL: Aprendizaje Supervisado
    path('preProcesamiento', views.preProcesamiento, name='preProcesamiento'),
    # URL: Aprendizaje Supervisado
    path('supervisado', views.supervisado, name='supervisado'),
    # URL: Aprendizaje No Supervisado
    path('noSupervisado', views.noSupervisado, name='noSupervisado'),
]
