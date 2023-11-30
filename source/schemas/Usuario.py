from bson import ObjectId
from pydantic import Field, BaseModel

from source.schemas.PyObjectIdSchema import PyObjectId


class Usuario(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    nome: str = Field(...)
    email: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "new_user",
                "nome": "New User",
                "email": "newuser@gmail.com"
            }
        }
