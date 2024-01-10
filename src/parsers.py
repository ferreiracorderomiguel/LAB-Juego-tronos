def parsea_bool_atacante(cadena):
    return True if cadena == "win" else False

def parsea_bool_mp(cadena):
    return True if cadena == "1" else False

def parsea_lista_comandantes(cadena):
    cadena = cadena.replace('"', '')
    lista = cadena.split(',')
    return [elem.strip() for elem in lista]

def parsea_num_opcional(cadena):
    return int(cadena) if cadena else None
