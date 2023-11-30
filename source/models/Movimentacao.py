from pydantic import BaseModel


class Movimentacao(BaseModel):
    data: str
    descricao: str
