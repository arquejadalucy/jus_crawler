from pydantic import BaseModel, validator


class ProcessRequestBody(BaseModel):
    numero_processo: str

    @validator("numero_processo", pre=True)
    def strip_numero_processo(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value
