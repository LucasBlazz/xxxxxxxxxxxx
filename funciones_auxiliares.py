# desicion tree


from collections import Counter
from itertools import islice


import pandas as pd




"""
Funcion genero.
Resumen: Devuelve los 5 generos mas publicados del año. 
Parametros: Año: string
Columnas a utilizar: "year_release" y "genre"
Retorna: Diccionario con la siguiente forma:
    {
    "Nombre genero":"cuantos veces se repite"
    }
"""

"""
Funcion juegos.
Resumen: Devuelve todos los juegos lanzados ese año. 
Parametros: Año: string
Columnas a utilizar: "year_release", "app_name" y "title"
Retorna: Diccionario con la siguiente forma:
    {
    "Año":["todos los juegos"]
    }
"""




# Comentar cada funcion

def aplanar_lista(lista):
    resultado = []
    for elemento in lista:
        if isinstance(elemento, list):
            resultado.extend(aplanar_lista(elemento))
        else:
            resultado.append(elemento)
    return resultado


def contar_elementos_repetidos(lista):
    conteo = Counter(elem for elem in lista if isinstance(elem, str))
    return dict(conteo.most_common())


def obtener_primeros_cinco_items(diccionario):
    primeros_cinco_items = dict(islice(diccionario.items(), 5))
    return primeros_cinco_items


def contiene_DLC(valor):
    if isinstance(valor, str):
        return "Downloadable Content" in valor
    elif isinstance(valor, list):
        return any("Downloadable Content" in elem for elem in valor)
    return False

