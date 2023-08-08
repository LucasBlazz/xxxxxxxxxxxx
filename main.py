from enum import Enum

from fastapi import FastAPI
import pandas as pd
import joblib

import funciones_auxiliares as fa
from data_preprocesada import df_genero, df_juegos, df_specs, df_early_access, df_sentiment, df_metascore
from eda import rmse

"""
TODO:
    - Agregar el path parameter a las def
    - Retornar mensaje cuando sea nulo
    - Documentar api
"""


app = FastAPI()


modelo = joblib.load("modelo_precio_videojuego.pkl")


class OpcionGenero(str, Enum):

    Accounting = "Accounting"
    Action = "Action"
    Adventure = "Adventure"
    Animation_and_Modeling = "Animation and Modeling"
    Audio_Production = "Audio Production"
    Casual = "Casual"
    Design_and_Illustration = "Design and Illustration"
    Education = "Education"
    Free_to_Play = "Free to Play"
    Indie = "Indie"
    Massively_Multiplayer = "Massively Multiplayer"
    Photo_Editing = "Photo Editing"
    rpg = "RPG"
    Racing = "Racing"
    Simulation = "Simulation"
    Software_Training = "Software Training"
    Sports = "Sports"
    Strategy = "Strategy"
    Utilities = "Utilities"
    Video_Production = "Video Production"
    Web_Publishing = "Web Publishing"



@app.get("/genero")
async def genero(anio: int):

    mascara = df_genero["year_release"] == anio
    df_temporal = df_genero[mascara]
    lista_anidada = list(df_temporal["genres"])
    lista_plana = fa.aplanar_lista(lista_anidada)
    cantidad_generos = fa.contar_elementos_repetidos(lista_plana)
    response = fa.obtener_primeros_cinco_items(cantidad_generos)
    
    return response


@app.get("/juegos")
async def juegos(anio: int):
    
    filtro_anio = df_juegos["year_release"] == anio
    df_temp = df_juegos[filtro_anio]
    lista_juegos = list(df_temp["app_name"])
    response = {f"Año: {anio}":lista_juegos}

    return response


@app.get("/specs")
async def specs(anio: int):
    
    mascara = df_specs["year_release"] == anio
    df_temp = df_specs[mascara]
    lista_anidada = list(df_temp["specs"])
    lista_plana = fa.aplanar_lista(lista_anidada)
    cantidad_specs = fa.contar_elementos_repetidos(lista_plana)
    response = fa.obtener_primeros_cinco_items(cantidad_specs)

    return response


@app.get("/earlyaccess")
async def early_access(anio: int):

    filtro_anio = df_early_access["year_release"] == anio
    df_temp = df_early_access[filtro_anio]
    response = {"Año:":anio,"Cantidad de juegos lanzados en early access": int(df_temp.shape[0])}

    return response


@app.get("/sentiment")
async def sentiment(anio: int):
    
    filtro_anio = df_sentiment["year_release"] == anio
    df_temp = df_sentiment[filtro_anio]
    response = fa.contar_elementos_repetidos(df_temp["sentiment"])
    return response


@app.get("/metascore")
async def metascore(anio: int):
    
    filtro_anio = df_metascore["year_release"] == anio
    df_temp = df_metascore[filtro_anio]
    df_temp.sort_values(by=["metascore"],ascending=False,inplace=True)
    df_temp_top = df_temp[["app_name","metascore"]].head(5)
    top_app_name = list(df_temp_top["app_name"])
    top_score = list(df_temp_top["metascore"])

    response = {}

    for name, score in zip(top_app_name,top_score):
        response[name] = score

    return response

@app.get("/prediccion")
async def predict(genero: OpcionGenero, early_access: bool):

    datos_entrada = {
    'early_access': [int(early_access)]
    }
    for opcion in OpcionGenero:
        datos_entrada[opcion.value] = [1 if opcion == genero else 0]
    df = pd.DataFrame(datos_entrada)
    
    prediccion = modelo.predict(df)

    return {
        "Predicción precio": f"{round(prediccion[0],2)} Dólares",
        "RMSE":rmse
        }