from bson import ObjectId
from pydantic import Field, BaseModel

from source.schemas.PyObjectIdSchema import PyObjectId


class Processo(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cnj: str = Field(...)
    tribunal: str = Field(...)
    polo_ativo: str = Field(...)
    polo_passivo: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "cnj": "0710802-55.2018.8.02.0001",
                "tribunal": "TJSP",
                "polo_ativo": "José Maria",
                "polo_passivo": "Maria José"
            }
        }
