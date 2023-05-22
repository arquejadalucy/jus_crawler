from pydantic import BaseModel


class ProcessoRequestBody(BaseModel):
    numero_processo: str