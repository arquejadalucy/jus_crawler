from cerberus import Validator
from fastapi import FastAPI

from app.crawler import search_process_data
from app.models import ProcessRequestBody, ProcessRequestInformations
from app.schemas import process_request_informations_schema, id_processo_schema

app = FastAPI()
validator = Validator()


def valid_request(processo_info: ProcessRequestInformations):
    return validator.validate(processo_info.__dict__, process_request_informations_schema)


def valid_process_id(numero_processo: str):
    return validator.validate({"id": numero_processo}, id_processo_schema)


@app.post("/processo")
async def buscar_processo(process_request: ProcessRequestBody):
    if not valid_process_id(process_request.numero_processo):
        return validator.errors

    processo_info = ProcessRequestInformations(process_request.numero_processo)

    if not valid_request(processo_info):
        return validator.errors

    response = await search_process_data(processo_info)
    return response


@app.get("/processo/{id_processo}")
async def get_processo_info_by_id(id_processo: str):
    if not valid_process_id(id_processo):
        return validator.errors

    processo_info = ProcessRequestInformations(id_processo)

    if not valid_request(processo_info):
        return validator.errors
    return await search_process_data(processo_info)
