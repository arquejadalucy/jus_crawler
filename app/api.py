import asyncio

from cerberus import Validator
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.crawler import search_process_data
from app.models import ProcessRequestBody, ProcessRequestInformations
from app.schemas import process_request_informations_schema, id_processo_schema

app = FastAPI()
validator = Validator()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


def valid_request(processo_info: ProcessRequestInformations):
    return validator.validate(processo_info.__dict__, process_request_informations_schema)


def valid_process_id(numero_processo: str):
    return validator.validate({"id": numero_processo}, id_processo_schema)


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def main(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.post('/dadosprocesso', include_in_schema=False)
def busca_processo_por_form(id_processo: str = Form(...)):
    if not valid_process_id(id_processo):
        return validator.errors

    processo_info = ProcessRequestInformations(id_processo)

    if not valid_request(processo_info):
        return validator.errors
    return search_process_data(processo_info)


@app.post("/processo")
async def buscar_processo(process_request: ProcessRequestBody):
    if not valid_process_id(process_request.numero_processo):
        return validator.errors

    processo_info = ProcessRequestInformations(process_request.numero_processo)

    if not valid_request(processo_info):
        return validator.errors

    response = await search_process_data(processo_info)
    return response


@app.get("/processos/{id_processo}")
def get_processo_info_by_id(id_processo: str):
    if not valid_process_id(id_processo):
        return validator.errors

    processo_info = ProcessRequestInformations(id_processo)

    if not valid_request(processo_info):
        return validator.errors
    return search_process_data(processo_info)
    # return templates.TemplateResponse("process.html", {"request": processo_info, "dados": search_process_data(processo_info)})
