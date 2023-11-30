from pydantic import BaseModel

from source.models.ProcessoInfo import ProcessoInfo


class Processo(BaseModel):
    cnj: str
    info_primeiro_grau: ProcessoInfo
    info_segundo_grau: ProcessoInfo
