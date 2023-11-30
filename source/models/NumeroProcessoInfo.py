class NumeroProcessoInfo(object):
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
