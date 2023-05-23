from pydantic import BaseModel


class ProcessRequestBody(BaseModel):
    numero_processo: str


class Parte(BaseModel):
    nome: str
    tipo_de_participacao: str


class ParteComAdvogados(Parte):
    advogados: list


class ProcessRequestInformations(object):
    numero_processo: str
    foro: str
    numeroDigitoAnoUnificado: str
    tribunal: str

    def __init__(self, numero_processo):
        self.numero_processo = numero_processo
        infos = numero_processo.split(".")
        self.foro = numero_processo[-1]
        self.numeroDigitoAnoUnificado = infos[0] + "." + infos[1]
        self.tribunal = infos[3]
