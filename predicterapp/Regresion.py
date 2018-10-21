from sklearn.kernel_ridge import KernelRidge
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def regresionPolinomial(nombreDatos, datosAdicionales, ventana, fechaInicioTrain, fechaFinTrain, fechaInicioTest, fechaFinTest):
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
    
    '''Creamos una matriz con todo el conjunto de datos y le asignamos la ventana para poder predecir el dia de manana'''
    vector = [0.75866803,  0.74066392,  0.72266718,  0.72266718, 0.75866803,  0.74066392,  0.72266718,  0.72266718, 0.75866803]
    prediccion = clf.predict([vector])
    
    
    return score, prediccion


def creacionMatrizDeRegresion(datosArrayClass, datosInferClass, datosAdicionales, fechaInicioTrain, fechaFinTrain, fechaInicioTest, fechaFinTest, ventana):
    
    '''Creamos los vectores correspondientes al conjunto de entrenamiento y al de pruebas'''
    vectorTrain = vectorDatosEntreAmbasFechas(datosArrayClass, datosInferClass, fechaInicioTrain, fechaFinTrain)
    vectorTest = vectorDatosEntreAmbasFechas(datosArrayClass, datosInferClass, fechaInicioTest, fechaFinTest)
    
    '''Creamos las matrices correspondientes a los vectores de entrenamiento y a los de pruebas'''
    matrizTrain = crearMatriz(vectorTrain, ventana)
    matrizTest = crearMatriz(vectorTest, ventana)
    
    if len(datosAdicionales) != 0:
        for aux in datosAdicionales:
            '''Leemos los datos'''
            ruta = '\predicterapp\static\predicterapp\myDates\dataframe\\' + aux + '.infer';
            datosInferAdicionales = pd.read_pickle(BASE_DIR + ruta)
            datosArrayAdicionales = np.load(BASE_DIR + '\\predicterapp\\static\\predicterapp\\myDates\\narray\\' + aux + '.npy')
            
            '''Creamos los vectores correspondientes al conjunto de entrenamiento y al de pruebas'''
            vectorTrainAdicionales = vectorDatosEntreAmbasFechas(datosArrayAdicionales, datosInferAdicionales, fechaInicioTrain, fechaFinTrain)
            vectorTestAdicionales = vectorDatosEntreAmbasFechas(datosArrayAdicionales, datosInferAdicionales, fechaInicioTest, fechaFinTest)
            
            '''Creamos las matrices correspondientes a los vectores de entrenamiento y a los de pruebas'''
            matrizTrainAdicionales = crearMatriz(vectorTrainAdicionales, ventana)
            matrizTestAdicionales = crearMatriz(vectorTestAdicionales, ventana)
            
            '''Nos quedamos con la X que es lo unico que nos interesa de las matrices creadas con los datos adicionales'''
            X_trainAdicionales = np.delete(matrizTrainAdicionales, matrizTrainAdicionales[0].size-1, 1)
            X_testAdicionales = np.delete(matrizTestAdicionales, matrizTestAdicionales[0].size-1, 1)
            
            '''Unimos le conjunto de datos adicionales'''
            matrizTrain = np.concatenate((X_trainAdicionales, matrizTrain), axis = 1)
            matrizTest = np.concatenate((X_testAdicionales, matrizTest), axis = 1)
    
    return matrizTrain, matrizTest

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
    dimension = X.shape
    vector = X[dimension[0]-1][1:]
    vector = np.insert(vector, vector.size,Y[dimension[0]-1])
    return vector