import json

from fastapi import FastAPI

from crawler import search_process_data
from models import ProcessRequestBody, ProcessRequestInformations

app = FastAPI()



@app.post("/processo")
def buscar_processo(process_request: ProcessRequestBody):
    processo_info = ProcessRequestInformations(process_request.numero_processo)
    return search_process_data(processo_info)


@app.get("/processo/{id_processo}")
def buscar_processo(id_processo: str):
    processo_info = ProcessRequestInformations(id_processo)
    return search_process_data(processo_info)