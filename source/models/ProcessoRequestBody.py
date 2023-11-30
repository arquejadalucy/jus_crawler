from pydantic import BaseModel


class ProcessRequestBody(BaseModel):
    numero_processo: str
