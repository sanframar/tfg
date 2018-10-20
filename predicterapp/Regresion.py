from sklearn.kernel_ridge import KernelRidge
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def regresionPolinomial(nombreDatos, datosAdicionales, numerosDiasAPredecir, fechaInicioTrain, fechaFinTrain, fechaInicioTest, fechaFinTest):
    '''Leemeos los datos almacenados'''
    ruta = '\predicterapp\static\predicterapp\myDates\dataframe\\' + nombreDatos + '.infer';
    datosInfer = pd.read_pickle(BASE_DIR + ruta)
    
    datosArray = np.load(BASE_DIR + '\\predicterapp\\static\\predicterapp\\myDates\\narray\\' + nombreDatos + '.npy')
    
    '''Creamos los vectores correspondientes al conjunto de entrenamiento y al de pruebas'''
    vectorTrain = vectorDatosEntreAmbasFechas(datosArray, datosInfer, fechaInicioTrain, fechaFinTrain)
    vectorTest = vectorDatosEntreAmbasFechas(datosArray, datosInfer, fechaInicioTest, fechaFinTest)
    
    '''Creamos las matrices correspondientes a los vectores de entrenamiento y a los de pruebas'''
    matrizTrain = crearMatriz(vectorTrain, numerosDiasAPredecir)
    matrizTest = crearMatriz(vectorTest, numerosDiasAPredecir)
    
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
    
    '''Creamos una matriz con todo el conjunto de datos y le asignamos la ventana para poder predecir el dia de manana'''
    matrizCompleta = crearMatriz(datosArray, numerosDiasAPredecir)
    Y = matrizCompleta[:,matrizCompleta[0].size-1]
    print(Y)
    X = np.delete(matrizCompleta, matrizCompleta[0].size-1, 1)
    print(X)
    vector = seleccionarVectorPredecir(Y,X)
    print(vector)
    prediccion = clf.predict([vector])
    
    
    return score, prediccion
    
    #return  clf.predict(numerosDiasAPredecir)



def crearMatriz(datos, ventana):
    ventana = int(ventana)
    matriz = np.zeros((datos.size, ventana+1))
    for x in range(ventana+1):
        vector = crearVector(datos, x)
        matriz[:,ventana-x] = vector[:,0]
    return matriz[ventana:vector.size :,]

def crearVector(vector, desplazamiento):
    result = vector[0:vector.size-1-desplazamiento+1]
    for aux in range(desplazamiento):
        result = np.insert(result, 0, 0)
    return result.reshape(-1, 1)

def buscarFecha(datosInfer, fecha):
    dt = pd.to_datetime(fecha)
    return datosInfer.index.get_loc(dt, method='nearest')

def vectorDatosEntreAmbasFechas(datosArray, datosInfer, fechaInicio, fechaFin):
    indiceFechaInicio = buscarFecha(datosInfer, fechaInicio)
    indiceFechaFin = buscarFecha(datosInfer,fechaFin)
    
    return datosArray[indiceFechaInicio: indiceFechaFin]

def seleccionarVectorPredecir(Y, X):
    vector = X[0][1:]
    vector = np.insert(vector, vector.size,Y[0])
    return vector