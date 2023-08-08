from enum import Enum

from fastapi import FastAPI, Path 
import pandas as pd
import joblib

import funciones_auxiliares as fa
from data_preprocesada import df_genero, df_juegos, df_specs, df_early_access, df_sentiment, df_metascore
from data_preprocesada import anio_mas_antiguo, anio_mas_reciente
from eda import rmse

"""
TODO:
    - Agregar el path parameter a las def
    - Retornar mensaje cuando sea nulo
    - Documentar api
"""




app = FastAPI(
    title="PI MLOps",
    version="1.0.0",
    description="Resolución del primer proyecto individual por Lucas Ramos. GITHUB https://github.com/LucasBlazz",
)


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



@app.get(
    path="/genero/{year}",
    summary="Los 5 generos más publicados en el año",
    tags=["Endpoints"]
    )
async def genero(
    year: int = Path(
    title="Año",
    ge= anio_mas_antiguo,
    le= anio_mas_reciente,
    example=2016
    )
):
    """Los 5 generos que mas se repitieron en el año

    Argumentos:
        year (int): Año

    Ejemplo de retorno:

        {
            "Indie": 2826,
            "Action": 2030,
            "Adventure": 1499,
            "Casual": 1217,
            "Simulation": 1173
        }
        
    """
    mascara = df_genero["year_release"] == year
    df_temporal = df_genero[mascara]
    lista_anidada = list(df_temporal["genres"])
    lista_plana = fa.aplanar_lista(lista_anidada)
    cantidad_generos = fa.contar_elementos_repetidos(lista_plana)
    response = fa.obtener_primeros_cinco_items(cantidad_generos)
    
    return response


@app.get(
    path="/juegos/{year}",
    summary="Todos los juegos lanzados en el año",
    tags=["Endpoints"]
    )
async def juegos(
    year: int = Path(
    title="Año",
    ge= anio_mas_antiguo,
    le= anio_mas_reciente,
    example=2004
    )
):
    """Todos los juegos lanzados en el año

    Argumentos
        year (int): Año

    Ejemplo de retorno:

        {
            "Año: 2004": [
            "Rome: Total War™ - Collection",
            "Manhunt",
            "Far Cry®",
            "Port Royale 2",
            ...]
        }
    
    """
    
    filtro_year = df_juegos["year_release"] == year
    df_temp = df_juegos[filtro_year]
    lista_juegos = list(df_temp["app_name"])
    response = {f"Año: {year}":lista_juegos}

    return response


@app.get(
    path="/specs/{year}",
    summary="Las caracteristicas que más se repitieron en el año",
    tags=["Endpoints"]
    )
async def specs(
    year: int = Path(
    title="Año",
    ge= anio_mas_antiguo,
    le= anio_mas_reciente,
    example=2017
    )
):
    """
    Las 5 especificaciones más repetidas del año

    Argumentos
        year (int): Año

    Ejemplo de retorno:

        {
            "Single-player": 7922,
            "Steam Achievements": 4994,
            "Downloadable Content": 3983,
            "Steam Trading Cards": 3309,
            "Steam Cloud": 2745
        }"""
    
    mascara = df_specs["year_release"] == year
    df_temp = df_specs[mascara]
    lista_anidada = list(df_temp["specs"])
    lista_plana = fa.aplanar_lista(lista_anidada)
    cantidad_specs = fa.contar_elementos_repetidos(lista_plana)
    response = fa.obtener_primeros_cinco_items(cantidad_specs)

    return response


@app.get(
    path="/earlyaccess/{year}",
    summary="Cantidad de juegos en acceso anticipado",
    tags=["Endpoints"]
    )
async def early_access(
    year: int = Path(
    title="Año",
    ge= anio_mas_antiguo,
    le= anio_mas_reciente,
    example=2018
    )
):
    """
    La cantidad de juegos lanzados en estado de early access

    Argumentos
        year (int): Año

    Ejemplo de retorno:

        {
            "Año:": 2018,
            "Cantidad de juegos lanzados en early access": 21
        }"""
    

    filtro_year = df_early_access["year_release"] == year
    df_temp = df_early_access[filtro_year]
    response = {"Año:":year,"Cantidad de juegos lanzados en early access": int(df_temp.shape[0])}

    return response


@app.get(
        path="/sentiment/{year}",
        summary="Reviews publicadas en el año",
        tags=["Endpoints"]
        )
async def sentiment(
    year: int = Path(
    title="Año",
    ge= anio_mas_antiguo,
    le= anio_mas_reciente,
    example=2000
    )
):
    """
    El tipo y la cantidad de reviews que se publicaron

    Argumentos
        year (int): Año

    Ejemplo de retorno:

        {
            "Very Positive": 12,
            "Mostly Positive": 7,
            "Mixed": 7,
            "Overwhelmingly Positive": 3,
            "Positive": 3,
            "Negative": 1
        } """
    
    filtro_year = df_sentiment["year_release"] == year
    df_temp = df_sentiment[filtro_year]
    response = fa.contar_elementos_repetidos(df_temp["sentiment"])

    return response


@app.get(
        path="/metascore/{year}",
        summary="Los mejores 5 juegos del año",
        tags=["Endpoints"])
async def metascore(
    year: int = Path(
    title="Año",
    ge= anio_mas_antiguo,
    le= anio_mas_reciente,
    example=2015
    )
):
    """
    Los 5 juegos con mejor puntuación del año

    Argumentos
        year (int): Año

    Ejemplo de retorno:

        {
            "Grand Theft Auto V": 96,
            "Divinity: Original Sin - Enhanced Edition": 94,
            "Undertale": 92,
            "METAL GEAR SOLID V: THE PHANTOM PAIN": 91,
            "Pillars of Eternity": 89
        } """    
    filtro_year = df_metascore["year_release"] == year
    df_temp = df_metascore[filtro_year]
    df_temp.sort_values(by=["metascore"],ascending=False,inplace=True)
    df_temp_top = df_temp[["app_name","metascore"]].head(5)
    top_app_name = list(df_temp_top["app_name"])
    top_score = list(df_temp_top["metascore"])

    response = {}

    for name, score in zip(top_app_name,top_score):
        response[name] = score

    return response


@app.get(
        path="/prediccion",
        summary="Predición de precios",
        tags=["Modelo predictivo"])
async def predict(genero: OpcionGenero, early_access: bool):
    """Modelo de predicción de precios de juegos

    Argumentos:
        genero (OpcionGenero): El genero del juego.

        early_access (bool): Si el juego a predecir se encuentra en acceso anticipado o no.

    Retorna:
        El valor predecido y el RMSE del modelo. Ejemplo de retorno:

        {
            "Predicción precio": "11.2 Dólares",
            "RMSE": 8.424571637950317
        }
    """

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