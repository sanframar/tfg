import pandas_datareader.data as web
from sklearn.preprocessing import StandardScaler
import datetime
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#Metodo que devuelve un array con los indices de los valores nulos del dataframe (NaN)
def indicesNulos(dataframe):
    indicesNaN = pd.isnull(dataframe).any(1).nonzero()[0]
    #Modificamos el orden del array para que calcule primero los valores de los extremos
    a = indicesNaN[indicesNaN.size-1:]
    b = indicesNaN[:1]
    c = indicesNaN[1:-1]
    indicesNaN = np.concatenate((b,a,c),axis=0)
    return indicesNaN
    
#Metodo que devuelve un array con los elementos normalizados entre los valores 0 y 1
def normalizacionDataframe(dataframe):
    stdsclr = StandardScaler()
    return stdsclr.fit_transform(dataframe)

#Metodo que calcula los nuevos valores para eliminar los NaN de nuestro conjunto de datos
def calcularValoresNaN(array, indicesNaN):
    for aux in indicesNaN:
        if(aux==0):
            nanEnInicio(array, indicesNaN, aux)
        if(aux==array.size-1):
            nanEnFinal(array, indicesNaN, aux)
        if((aux>0) & (aux<array.size-1)):
            nanEnMedio(array, indicesNaN, aux)
    return array
            
def nanEnInicio(array, indicesNaN, aux):
    for idx, value in enumerate(range(0,11)):
        if(np.isnan(array[aux+idx+1]) != True):
            nextValue = array[aux+idx+1]
            nextIndice = aux+idx+1
            break
        
    for idx, value in enumerate(range(0,11)):
        if(np.isnan(array[idx+nextIndice+1]) != True):
            nextValue2 = array[idx+nextIndice+1]
            nextIndice2 = idx+nextIndice+1
            break
    
    newValue = (nextValue + nextValue2)/2
    print(newValue)
    array[aux] = newValue
    
def nanEnFinal(array, indicesNaN, aux):
    for idx, value in enumerate(range(0,11)):
        if(np.isnan(array[aux-idx-1]) != True):
            nextValue = array[aux-idx-1]
            nextIndice = aux-idx-1
            break
            
    for idx, value in enumerate(range(0,11)):
        if(np.isnan(array[nextIndice-idx-1]) != True):
            nextValue2 = array[nextIndice-idx-1]
            nextIndice2 = nextIndice-idx-1
            break
            
    newValue = (nextValue + nextValue2)/2
    print(newValue)
    array[aux] = newValue

def nanEnMedio(array, indicesNaN, aux):
    for idx, value in enumerate(range(0,11)):
        if(np.isnan(array[aux+idx+1]) != True):
            nextValue = array[aux+idx+1]
            nextIndice = aux+idx+1
            break
            
    for idx, value in enumerate(range(0,11)):
        if(np.isnan(array[aux-idx-1]) != True):
            afterValue = array[aux-idx-1]
            afterIndice = aux-idx-1
    
    newValue = (nextValue + afterValue)/2
    print(newValue)
    array[aux] = newValue