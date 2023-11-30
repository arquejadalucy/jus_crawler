from enum import Enum


class Tribunais(str, Enum):
    TJAL = "02"
    TJSP = "26"
    #TJCE = "06" #não funciona async


TRIBUNAIS_VALIDOS = [tribunal.value for tribunal in Tribunais]


class DominiosPorTribunal(str, Enum):
    TJAL = "www2.tjal.jus.br"
    TJSP = "esaj.tjsp.jus.br"
    #TJCE = "esaj.tjce.jus.br" #não funciona async

