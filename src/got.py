import csv
from typing import List, NamedTuple, Optional
from parsers import *


BatallaGOT = NamedTuple('BatallaGOT',
    [('nombre', str), ('rey_atacante', str), ('rey_atacado', str), ('gana_atacante', bool),
     ('muertes_principales', bool), ('comandantes_atacantes', List[str]), ('comandantes_atacados', List[str]),
     ('region', str), ('num_atacantes', Optional[int]), ('num_atacados', Optional[int])])

def lee_batallas(ruta_fichero: str) -> List[BatallaGOT]:
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