from collections import defaultdict
import csv
from typing import List, NamedTuple, Optional, Tuple
from parsers import *


BatallaGOT = NamedTuple('BatallaGOT',
    [('nombre', str), ('rey_atacante', str), ('rey_atacado', str), ('gana_atacante', bool),
     ('muertes_principales', bool), ('comandantes_atacantes', List[str]), ('comandantes_atacados', List[str]),
     ('region', str), ('num_atacantes', Optional[int]), ('num_atacados', Optional[int])])

def lee_batallas(ruta_fichero: str) -> List[BatallaGOT]:
    '''
    Lee un fichero de entrada en formato CSV codificado en utf-8 y devuelve una
    lista de tuplas de tipo BatallaGOT conteniendo todos los datos almacenados
    en el fichero. Use el método de cadenas split para separar los comandantes
    atacantes y atacados, y el método de cadenas strip para eliminar los
    espacios al inicio o final de los nombres de los comandantes. (1,25 puntos)
    '''
    res = []

    with open(ruta_fichero, encoding="UTF-8") as f:
        lector = csv.reader(f, delimiter=",")
        next(lector)

        for nombre, rey_atacante, rey_atacado, gana_atacante, muertes_principales, comandantes_atacantes, comandantes_atacados, region, num_atacantes, num_atacados in lector:
            nombre = nombre.strip()
            rey_atacante = rey_atacante.strip()
            rey_atacado = rey_atacado.strip()
            gana_atacante = parsea_bool_atacante(gana_atacante)
            muertes_principales = parsea_bool_mp(muertes_principales)
            comandantes_atacantes = parsea_lista_comandantes(comandantes_atacantes)
            comandantes_atacados = parsea_lista_comandantes(comandantes_atacados)
            region = region.strip()
            num_atacantes = parsea_num_opcional(num_atacantes)
            num_atacados = parsea_num_opcional(num_atacados)

            res.append(BatallaGOT(nombre, rey_atacante, rey_atacado, gana_atacante, muertes_principales, comandantes_atacantes, comandantes_atacados, region, num_atacantes, num_atacados))

    return res 

def reyes_mayor_menor_ejercito(batallas: List[BatallaGOT]) -> Tuple[str, str]:
    '''
    Recibe una lista de tuplas de tipo BatallaGOT y devuelve una tupla con dos cadenas
    correspondientes a los nombres de los reyes con el mayor y el menor ejército,
    respectivamente, del acumulado de todas las batallas. Para calcular el tamaño del
    ejército de un rey se deben sumar los números de atacantes o de atacados de todas
    las batallas en las que ha participado dicho rey como atacante o como atacado.
    (2 puntos)
    '''
    batallas_reyes = defaultdict(int)

    for batalla in batallas:
        if batalla.num_atacantes != None:
            batallas_reyes[batalla.rey_atacante] += batalla.num_atacantes
        if batalla.num_atacados != None:
            batallas_reyes[batalla.rey_atacado] += batalla.num_atacados

    rey_mayor_ejercito = max(batallas_reyes, key = batallas_reyes.get)
    rey_menor_ejercito = min(batallas_reyes, key = batallas_reyes.get)

    
    return (rey_mayor_ejercito, rey_menor_ejercito)