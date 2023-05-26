from cerberus import Validator
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.crawler import search_process_data
from app.models import ProcessRequestBody, ProcessRequestInformations
from app.schemas import process_request_informations_schema, id_processo_schema, ProcessNumberRegexErrorHandler

app = FastAPI()
validator = Validator(error_handler=ProcessNumberRegexErrorHandler)


def valid_request(processo_info: ProcessRequestInformations):
    return validator.validate(processo_info.__dict__, process_request_informations_schema)


def valid_process_id(numero_processo: str):
    return validator.validate({"numero_processo": numero_processo}, id_processo_schema)


@app.post("/processo")
def buscar_processo(process_request: ProcessRequestBody):
    if not valid_process_id(process_request.numero_processo):
        return validator.errors

    processo_info = ProcessRequestInformations(process_request.numero_processo)

    if not valid_request(processo_info):
        return validator.errors

    response = search_process_data(processo_info)
    return response


@app.get("/processo/{id_processo}")
def get_processo_info_by_id(id_processo: str):
    if not valid_process_id(id_processo):
        return validator.errors

    processo_info = ProcessRequestInformations(id_processo)

    if not valid_request(processo_info):
        return validator.errors
    return search_process_data(processo_info)


def get_jinja_templates():
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    return Jinja2Templates(directory="app/templates")


@app.post('/buscaprocesso', include_in_schema=False)
def buscar_processo_pelo_form(request: Request, id_processo: str = Form()):
    result = get_processo_info_by_id(id_processo)
    return get_jinja_templates().TemplateResponse('processo.html', {'request': request, 'result': result})


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def main(request: Request):
    return get_jinja_templates().TemplateResponse('home.html', {'request': request})
