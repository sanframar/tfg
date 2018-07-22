'''
Created on 10 jul. 2018

@author: Santiago
'''
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datos', views.datos, name='datos'),
    # ex: /polls/5/results/
    path('supervisado', views.supervisado, name='supervisado'),
    # ex: /polls/5/vote/
    path('noSupervisado', views.noSupervisado, name='noSupervisado'),
]
