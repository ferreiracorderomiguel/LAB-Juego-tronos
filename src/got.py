from collections import defaultdict
import csv
from typing import Dict, List, NamedTuple, Optional, Set, Tuple
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

def batallas_mas_comandantes(batallas: List[BatallaGOT], regiones: Set[str]= None, n:int=None) -> List[Tuple[str, int]]:
    '''
    Recibe una lista de tuplas de tipo BatallaGOT, un conjunto de cadenas regiones,
    con valor por defecto None, y un valor entero n con valor por defecto None, y
    devuelve una lista de tuplas (str, int) con los nombres y el total de comandantes
    participantes de aquellas n batallas con mayor número de comandantes participantes
    (tanto atacantes como atacados), llevadas a cabo en alguna de las regiones
    indicadas en el parámetro regiones. Si el parámetro regiones es None se
    considerarán todas las regiones; por su parte, si el parámetro n es None se
    devolverán las tuplas correspondientes a todas las batallas de las regiones
    escogidas. En todos los casos, la lista devuelta estará ordenada de mayor a menor
    número de comandantes. (2 puntos)
    '''
    batallas_dict = defaultdict(int)
    for batalla in batallas:
        if regiones is None or batalla.region in regiones:
            batallas_dict[batalla.nombre] += len(batalla.comandantes_atacantes)
            batallas_dict[batalla.nombre] += len(batalla.comandantes_atacados)

    batallas_ordenadas = sorted(batallas_dict.items(), key=lambda item:item[1], reverse=True)
    return batallas_ordenadas if n is None else batallas_ordenadas[:n]

def rey_mas_victorias(batallas: List[BatallaGOT], rol:str="ambos") -> Tuple[str, int]:
    '''
    Recibe una lista de tuplas de tipo BatallaGOT y una cadena rol, con valor por
    defecto "ambos", y devuelve una tuplas con el nombre del rey que acumula mas
    victorias y el número de victorias conseguidas. Tenga en cuenta que un rey puede
    ganar una batalla en la que actúa como atacante, en cuyo caso el campo
    gana_atacante será True, o una batalla en la que actúa como atacado, en cuyo caso
    el campo gana_atacante será False. Si el parámetro rol es igual a "atacante", se
    devolverá el nombre del rey que acumula más victorias como atacante; si rol es
    igual a "atacado", se devolverá el nombre del rey que acumula más victorias como
    atacado; si rol es igual a "ambos", se devolveré el nombre del rey que acumula
    más victorias en todas las batallas en las que ha participado (sumando sus
    victorias como atacante y como atacado). Si ningún rey acumula victorias del rol
    especificado en la lista de batallas recibida, la función devuelve None. (2,75 puntos)
    '''
    reyes_dict = defaultdict(int)

    for batalla in batallas:
        if rol == "ambos":
            if batalla.gana_atacante:
                reyes_dict[batalla.rey_atacante] += 1
            else:
                reyes_dict[batalla.rey_atacado] += 1
        elif rol == "atacante":
            if batalla.gana_atacante:
                reyes_dict[batalla.rey_atacante] += 1
        elif rol == "atacado":
            if not batalla.gana_atacante:
                reyes_dict[batalla.rey_atacado] += 1

    rey_con_mas_victorias = max(reyes_dict.items(), key = lambda item:item[1])

    return rey_con_mas_victorias

def rey_mas_victorias_por_region(batallas: List[BatallaGOT], rol:str="ambos") -> Dict[str, str]:
    '''
    Recibe una lista de tuplas de tipo BatallaGOT y una cadena rol, con valor por defecto
    "ambos", y devuelve un diccionario que relaciona cada región con el nombre del rey o
    reyes que acumula más victorias en batallas ocurridas en esa región. El parámetro rol
    tiene el mismo significado que en la función anterior. Si para alguna región no hay
    ningún rey que haya ganado una batalla con el rol especificado, en el diccionario
    aparecerá el valor None asociado a dicha región. Puede usar la función
    rey_mas_victorias para resolver este ejercicio, pero recuerde que esta función puede
    devolver None en lugar de una tupla en la que estaría el que busca. (2 puntos)
    '''
    batallas_por_region = defaultdict(list)
    victorias_por_region = defaultdict(str)

    for batalla in batallas:
        batallas_por_region[batalla.region].append(batalla)
    
    for region, batallas in batallas_por_region.items():
        ganador = rey_mas_victorias(batallas)[0]
        victorias_por_region[region] = ganador

    return victorias_por_region