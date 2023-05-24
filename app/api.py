from cerberus import Validator
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.crawler import search_process_data
from app.models import ProcessRequestBody, ProcessRequestInformations

app = FastAPI()
validator = Validator()
#
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


@app.post("/processo")
def buscar_processo(process_request: ProcessRequestBody):
    processo_info = ProcessRequestInformations(process_request.numero_processo)
    # if not validator.validate(processo_info, process_request_informations_schema):
    #     return validator.errors

    response = search_process_data(processo_info)
    # if not validator.validate(response, process_response_payload_schema):
    #     return validator.errors
    return response


@app.get("/processo/{id_processo}")
def get_processo_info_by_id(id_processo: str):
    processo_info = ProcessRequestInformations(id_processo)
    return search_process_data(processo_info)
    # return templates.TemplateResponse("process.html", {"request": processo_info, "dados": search_process_data(processo_info)})
