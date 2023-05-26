from enum import Enum


class Tribunais(str, Enum):
    TJAL = "02"


TRIBUNAIS_VALIDOS = [tribunal.value for tribunal in Tribunais]


class DominiosPorTribunal(str, Enum):
    TJAL = "www2.tjal.jus.br"
