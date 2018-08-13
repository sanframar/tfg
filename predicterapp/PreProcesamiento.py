import pandas_datareader.data as web
from sklearn.preprocessing import StandardScaler
import datetime
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#Metodo que devuelve un array con los indices de los valores nulos del dataframe (NaN)
def indicesNulos(dataframe):
    return pd.isnull(dataframe).any(1).nonzero()[0]
    
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
        if(aux>0 & aux<array.size-1):
            nanEnMedio(array, indicesNaN, aux)
            
            
def nanEnInicio(array, indicesNaN, aux):
    nextValue = array[aux+1]
    nextValue2 = array[aux+2]
    newValue = (nextValue + nextValue2)/2
    print(newValue)
    array[aux] = newValue
    
def nanEnFinal(array, indicesNaN, aux):
    nextValue = array[aux-1]
    nextValue2 = array[aux-2]
    newValue = (nextValue + nextValue2)/2
    print(newValue)
    array[aux] = newValue

def nanEnMedio(array, indicesNaN, aux):
    nextValue = array[aux+1]
    afterValue = array[aux-1]
    newValue = (nextValue + afterValue)/2
    print(newValue)
    array[aux] = newValue