from sklearn.kernel_ridge import KernelRidge
import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_absolute_error
from predicterapp.Utils import *
from predicterapp.PreProcesamiento import desNormalizar
from predicterapp.Regresion import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def algoritmoClasificacion(nombreDatos, datosAdicionales, ventana, diasAPredecir, fechaInicioTrain, fechaFinTrain, fechaInicioTest, fechaFinTest, epsilon):
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
    
    '''Modificamos el resultado de nuestro conjunto de datos para clasificacion'''
    y_train = modificarYParaClasificacion(y_train, float(epsilon))
    y_test = modificarYParaClasificacion(y_test, float(epsilon))
    
    '''Declaramos nuestro algoritmo de regresion y lo entrenamos con el conjunto de entrenamiento'''
    neigh = seleccionarMejorAlgoritmoClasificacion(X_train, y_train, X_test, y_test)
    
    neigh.fit(X_train, y_train)
    
    '''Comprobamos como es de bueno nuestro algoritmo'''
    score = neigh.score(X_test, y_test)
    
    '''Creamos una matriz con todo el conjunto de datos y le asignamos la ventana para poder predecir el dia de manana'''
    
    matrizCompleta = crearMatrizRegresionCompleta(datosArrayClass, datosInferClass, datosAdicionales, ventana)
    Y = matrizCompleta[:,matrizCompleta[0].size-1]
    X = np.delete(matrizCompleta, matrizCompleta[0].size-1, 1)
    vector = X[0:1, :][0]
    
    prediccion = creacionVectoresParaPredecir(vector, int(float(diasAPredecir)), neigh)
    
    return score, prediccion



def aumenDismOIgual(valueAfter, valueNext, alfa):
    valueCalculate = valueNext-valueAfter
    if(valueCalculate>0 and valueCalculate>alfa):
        return 1
    if(valueCalculate<0 and abs(valueCalculate)>alfa):
        return -1
    if(abs(valueCalculate)<alfa):
        return 0
    
def modificarYParaClasificacion(datosArray, alfa):
    result = []
    for index, value in enumerate(datosArray):
        '''El primer valor vamos a suponer que no varia por lo que le ponemos un 0'''
        if(index==0):
            result.append(0)
        if(index>0):
            result.append(aumenDismOIgual(datosArray[index-1], value, alfa))
    return result

def seleccionarMejorAlgoritmoClasificacion(X_train, y_train, X_test, y_test):
    scores = {}
    '''Importacion de todos los algoritmos que vamos a implementar'''
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.linear_model import SGDClassifier
    from sklearn.linear_model import LogisticRegression
    
    '''Declaracion de los algoritmos y entrenamiento de los algortimos'''
    '''K-Neighbors'''
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(X_train, y_train)
    scoreNeigh = neigh.score(X_test, y_test)
    scores[neigh] = scoreNeigh
    
    '''Gaussian Naive Baye'''
    gaussianNaiveBaye = GaussianNB()
    gaussianNaiveBaye.fit(X_train, y_train)
    scoreGaussianNaiveBaye = gaussianNaiveBaye.score(X_test, y_test)
    scores[gaussianNaiveBaye] = scoreGaussianNaiveBaye
    
    '''Decision Tree Classifier'''
    decisionTree = DecisionTreeClassifier(random_state=0)
    decisionTree.fit(X_train, y_train)
    scoreDecisionTree = decisionTree.score(X_test, y_test)
    scores[decisionTree] = scoreDecisionTree
    
    '''Stochastic Gradient Descent Classification'''
    Sgcd = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
    Sgcd.fit(X_train, y_train)
    scoreSgcd = Sgcd.score(X_test, y_test)
    scores[Sgcd] = scoreSgcd
    
    '''Logistic Regression'''
    logisticRegression = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
    logisticRegression.fit(X_train, y_train)
    scoreLogisticRegression = logisticRegression.score(X_test, y_test)
    scores[logisticRegression] = scoreLogisticRegression
    
    import operator
    return max(scores.items(), key=operator.itemgetter(1))[0]