import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from ast import literal_eval

import joblib
#from funciones_auxiliares import *
rows = []
with open("dataset_raw/steam_games.json") as f:
    for line in f.readlines():
        rows.append(literal_eval(line))

df = pd.DataFrame(rows)

df.columns
# me quedo con las columnas que me interasan para le modelo
df_predict = df[["genres","early_access","price"]]
df_predict.info()
# viendo los nulos
#print("Generos nulos:",df_predict["genres"].isna().sum())
#print("Early access nulos",df_predict["early_access"].isna().sum())
#print("Precios nulos",df_predict["price"].isna().sum())

"""generos = list(df_predict["genres"])
generos =  aplanar_lista(generos)
generos_set = set(generos)
print(f"Hay {len(generos_set)} generos distintos")"""


# ni me acuerdo que hace esto preguntale a chat gpt
df_predict["price"] = df_predict["price"].apply(lambda x: 0 if isinstance(x, str) else x)
df_predict["price"].isna().sum()
df_predict.dropna(subset=["price"],inplace=True)
df_predict['price'] = df_predict["price"].apply(lambda x: float(x) if isinstance(x, (int, float)) else float('nan'))
df_predict["price"].astype("float")
df_predict["price"].dropna(inplace=True)

# Rellenamos los nulos de la columna con el promedio.
precio_medio = df_predict["price"].mean()
df_predict["price"].fillna(precio_medio,inplace=True)
df_predict["price"].describe()
# Debido a que el estandar en la industria el precio maximo de un videojuego es de 60 dolares, descartamos los valores por encima de este
filtro_outliers = df_predict["price"] <= 60
df_predict = df_predict[filtro_outliers]
df_predict.shape[0]
# Transformación del género utilizando codificación one-hot
generos_dummies = df_predict["genres"].str.join(",").str.get_dummies(sep=",")
df_predict= pd.concat([df_predict, generos_dummies], axis=1)

df_predict.drop(columns=["genres"],inplace=True)
df_predict.drop(columns=["Early Access"],inplace=True)
df_predict.columns
# Corregimos nombres de columnas
df_predict.rename(columns={"Animation &amp; Modeling":"Animation and Modeling","Design &amp; Illustration":"Design and Illustration"}, inplace=True)
df_predict.columns


X = df_predict.drop(columns=['price'])
y = df_predict["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()

# Entrenamos el modelo
model.fit(X_train,y_train)
y_pred = model.predict(X_test)

X_test
# Calculamos el error cuadratico medio para medir nuestro modelo
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
#print("RMSE:", rmse)
joblib.dump(model,"modelo_precio_videojuego.pkl")