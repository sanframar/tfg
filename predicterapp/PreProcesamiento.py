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