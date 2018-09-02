from sklearn.kernel_ridge import KernelRidge
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def regresionPolinomial(nombreDatos, numerosDiasAPredecir):
    '''Preparamos los datos para la creaciom del algoritmo de regresion'''
    '''CUIDADO, COGEMOS SOLO 100 VALORES PARA PROBARLO. ESTO HAY QUE MODIFICARLO'''
    Y = np.load(BASE_DIR + '\\predicterapp\\static\\predicterapp\\myDates\\narray\\' + nombreDatos + '.npy').reshape(1, -1)[0][0:100]
    X = np.arange(Y.size).reshape(-1, 1)
    
    '''Entrenamos el algoritmo con los datos proporcionados'''
    clf = KernelRidge(kernel="polynomial")
    clf.fit(X, Y)
    
    '''Predecimos los valores. OJO, ESTE METODO NO FUINCIONA CORRECTAMENTE Y SE DEBERA DE MODIFICAR EN EL FUTURO POR OTRO
    QUE FUNCIONE MEJOR'''
    #dias = []
    #for x in range(numerosDiasAPredecir):
    #    dias.append(Y.size + x)
    
    return  clf.predict(numerosDiasAPredecir)