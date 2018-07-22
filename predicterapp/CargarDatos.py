'''
Created on 22 jul. 2018

@author: Santiago
'''
import pandas_datareader.data as web
import datetime
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def obtenerDatosApi():
    try:
        dfCierre = pd.read_pickle(BASE_DIR + '\predicterapp\static\predicterapp\myDates\ibexCierre.infer')
        hayDatos = True
    except FileNotFoundError:
        hayDatos = False
    
    print (hayDatos)
    
    if (hayDatos==True) & (datosActualizado()==True):
        print('Todos los datos estan actualizados')
    
    elif (hayDatos==True) & (datosActualizado()==False):
        actualizarDatos()
        
    elif hayDatos==False:
        obtenicionDeDatos()
        
        
def datosActualizado():
    actualizado = True
    current = datetime.datetime.now()
    try:
        dfCierre = pd.read_pickle(BASE_DIR + '\predicterapp\static\predicterapp\myDates\ibexCierre.infer')
        ultimaFechaCierre = dfCierre.tail(1).reset_index()['Date'][0]
        if ultimaFechaCierre.date() < current.date():
            actualizado = False
    
    except:
        print(actualizado)
    
    return actualizado

def actualizarDatos():
    current = datetime.datetime.now()
    dfCierre = pd.read_pickle(BASE_DIR + '\predicterapp\static\predicterapp\myDates\ibexCierre.infer')
    ultimaFechaCierre = dfCierre.tail(1).reset_index()['Date'][0]
    
    f = web.DataReader("^IBEX", 'yahoo', ultimaFechaCierre, current)
    
    ibexCierre = f.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
    
    dfCierre = dfCierre.append(ibexCierre)
    
    dfCierre = dfCierre.drop_duplicates()
    
    dfCierre.to_pickle(BASE_DIR + '\predicterapp\static\predicterapp\myDates\ibexCierre.infer')
    
def obtenicionDeDatos():
    '''Seleccionamos las fechas de las que queremos obtener los datos'''
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime.now()
    
    '''Construimos la peticion a la api de yahoo'''
    f = web.DataReader("^IBEX", 'yahoo', start, end)
    
    '''Obtenemos los datos y los almacenamos en un dataframe'''
    ibexCierre = f.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
    
    '''Guardamos los datos en un fichero .infer para su posterior procesamiento, pero
    antes comprobamos que los ficheros no existen'''
   
    ibexCierre.to_pickle(BASE_DIR + '\predicterapp\static\predicterapp\myDates\ibexCierre.infer')
    