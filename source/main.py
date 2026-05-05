import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from source.controller.processos import get_processo_info_by_id
from source.controller import processos

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "front-end" / "static"
TEMPLATES_DIR = BASE_DIR / "front-end" / "templates"

app = FastAPI()
app.include_router(processos.router)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def get_jinja_templates():
    return templates


def normalize_process_result_for_template(id_processo: str, result):
    if not isinstance(result, dict):
        return {"id": id_processo, "ERROR": "Erro ao consultar processo"}

    if "id" in result:
        # If result has nested "Resultado" structure, flatten it
        if "Resultado" in result and isinstance(result["Resultado"], dict):
            normalized = {"id": result.get("id", id_processo)}
            normalized.update(result["Resultado"])
            return normalized
        return result

    error_message = "Erro ao consultar processo"
    for value in result.values():
        if isinstance(value, list) and value:
            error_message = value[0]
            break
        if isinstance(value, str) and value:
            error_message = value
            break

    return {"id": id_processo, "ERROR": error_message}


@app.get('/', response_class=HTMLResponse, tags=["home"], include_in_schema=False)
def main(request: Request):
    return get_jinja_templates().TemplateResponse('home.html', {'request': request})


@app.get('/sobre', response_class=HTMLResponse, tags=["about"], include_in_schema=False)
def about(request: Request):
    return get_jinja_templates().TemplateResponse('sobre.html', {'request': request})


@app.post('/buscaprocesso', include_in_schema=False)
def buscar_processo_pelo_form(request: Request, id_processo: str = Form()):
    result = get_processo_info_by_id(id_processo)
    normalized_result = normalize_process_result_for_template(id_processo, result)
    return get_jinja_templates().TemplateResponse('processo.html', {'request': request, 'result': normalized_result})


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
