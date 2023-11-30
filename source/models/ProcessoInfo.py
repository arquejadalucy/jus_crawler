from pydantic import BaseModel

from source.models import Movimentacao
from source.models.Parte import Parte


class ProcessoInfo(BaseModel):
    classe: str
    area: str
    assunto: str
    data: str
    juiz: str
    valor: str
    partes: list[Parte]
    movimentacoes: list[Movimentacao]
