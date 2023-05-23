from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.crawler import search_process_data
from app.models import ProcessRequestBody, ProcessRequestInformations

app = FastAPI()
#
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


@app.post("/processo")
def buscar_processo(process_request: ProcessRequestBody):
    processo_info = ProcessRequestInformations(process_request.numero_processo)
    return search_process_data(processo_info)


@app.get("/processo/{id_processo}", response_class=HTMLResponse)
def get_processo_info_by_id(id_processo: str):
    processo_info = ProcessRequestInformations(id_processo)
    return search_process_data(processo_info)
    # return templates.TemplateResponse("process.html", {"request": processo_info, "dados": search_process_data(processo_info)})
