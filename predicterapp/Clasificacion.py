from sklearn.kernel_ridge import KernelRidge
import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_absolute_error
from predicterapp.Utils import *
from predicterapp.PreProcesamiento import desNormalizar
from predicterapp.Regresion import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def regresionPolinomial(nombreDatos, datosAdicionales, ventana, diasAPredecir, fechaInicioTrain, fechaFinTrain, fechaInicioTest, fechaFinTest):
    '''Leemeos los datos almacenados'''
    ruta = '\predicterapp\static\predicterapp\myDates\dataframe\\' + nombreDatos + '.infer';
    datosInferClass = pd.read_pickle(BASE_DIR + ruta)
    
    datosArrayClass = np.load(BASE_DIR + '\\predicterapp\\static\\predicterapp\\myDates\\narray\\' + nombreDatos + '.npy')
    
    '''Creamos la matriz con todos los distintos conjuntos de datos seleccionados en el formulario'''
    matrizTrain, matrizTest = creacionMatrizDeRegresion(datosArrayClass, datosInferClass, datosAdicionales, fechaInicioTrain, fechaFinTrain, fechaInicioTest, fechaFinTest, ventana)
    
    print(matrizTrain.shape)
    print(matrizTest.shape)
    
    '''Dividimos nuestras matrices de entrenamiento y pruebas para poder entrenar el algoritmo'''
    y_train = matrizTrain[:,matrizTrain[0].size-1]
    X_train = np.delete(matrizTrain, matrizTrain[0].size-1, 1)
    y_test = matrizTest[:,matrizTest[0].size-1]
    X_test = np.delete(matrizTest, matrizTest[0].size-1, 1)
    
    '''Declaramos nuestro algoritmo de regresion y lo entrenamos con el conjunto de entrenamiento'''
    from sklearn.kernel_ridge import KernelRidge
    clf = KernelRidge(kernel="polynomial")
    clf.fit(X_train, y_train)
    
    '''Comprobamos como es de bueno nuestro algoritmo'''
    score = clf.score(X_test, y_test)
    mae = mean_absolute_error(y_test, clf.predict(X_test))
    
    '''Creamos una matriz con todo el conjunto de datos y le asignamos la ventana para poder predecir el dia de manana'''
    
    matrizCompleta = crearMatrizRegresionCompleta(datosArrayClass, datosInferClass, datosAdicionales, ventana)
    Y = matrizCompleta[:,matrizCompleta[0].size-1]
    X = np.delete(matrizCompleta, matrizCompleta[0].size-1, 1)
    vector = X[0:1, :][0]
    
    prediccion = creacionVectoresParaPredecir(vector, int(float(diasAPredecir)), clf)
    
    prediccion = desNormalizar(datosInferClass.tail(1).reset_index()['Close'][0], datosArrayClass[datosArrayClass.size-1], prediccion)
    
    
    return score, mae, prediccion
