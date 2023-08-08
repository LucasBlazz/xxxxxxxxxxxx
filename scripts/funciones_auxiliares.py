from collections import Counter
from itertools import islice

# Comentar cada funcion

def aplanar_lista(lista_anidada: list) -> list:
    """Desanida listas

    Ej: ["a",["b","c"]] -> ["a","b","c"]

    Args:
        lista_anidada (list)

    Returns:
        list:
    """
    resultado = []
    for elemento in lista_anidada:
        if isinstance(elemento, list):
            resultado.extend(aplanar_lista(elemento))
        else:
            resultado.append(elemento)
    return resultado


def contar_elementos_repetidos(lista: list) -> dict:
    """Cuenta elementos repetidos

    Ej: ["a","a","b"] -> {"a":2,"b":1}

    Args:
        lista (lista)

    Returns:
        Dict 
    """
    conteo = Counter(elem for elem in lista if isinstance(elem, str))
    return dict(conteo.most_common())


def obtener_primeros_cinco_items(diccionario: dict) -> dict:
    """Devuelve los 5 items con mayor value

    {"a":10,"b":9,"c":8,"d":7,"e":6,"f":5,"g":4,"h":3,"i":2,"j":1} -> {"a":10,"b":9,"c":8,"d":7,"e":6}


    Args:
        diccionario (_type_): _description_

    Returns:
        _type_: _description_
    """
    primeros_cinco_items = dict(islice(diccionario.items(), 5))
    return primeros_cinco_items


def contiene_DLC(valor: str):
    """Verifica si el se encuentra el atributo "Downloadable Content" en una lista

    Args:
        valor (str): elemento de una lista

    """
    if isinstance(valor, str):
        return "Downloadable Content" in valor
    elif isinstance(valor, list):
        return any("Downloadable Content" in elem for elem in valor)
    return False

