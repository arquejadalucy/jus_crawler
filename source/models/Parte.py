from bson import ObjectId

from source.services.dict_to_obj import DictObj


class Parte(object):
    nome: str
    tipo_de_participacao: str
    advogados: list

    def __init__(self, nome, tipo_de_participacao, advogados=None):
        self.nome = nome
        self.tipo_de_participacao = tipo_de_participacao
        self.advogados = advogados if advogados is not None else []
