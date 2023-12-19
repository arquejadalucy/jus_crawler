import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from source.controller.processos import get_processo_info_by_id
from source.controller import processos

app = FastAPI()
app.include_router(processos.router)


def get_jinja_templates():
    app.mount("/static", StaticFiles(directory="front-end/static"), name="static")
    app.mount("/templates", StaticFiles(directory="front-end/templates"), name="templates")
    return Jinja2Templates(directory="front-end/templates")


@app.get('/', response_class=HTMLResponse, tags=["home"], include_in_schema=False)
def main(request: Request):
    return get_jinja_templates().TemplateResponse('home.html', {'request': request})


@app.post('/buscaprocesso', include_in_schema=False)
def buscar_processo_pelo_form(request: Request, id_processo: str = Form()):
    result = get_processo_info_by_id(id_processo)
    return get_jinja_templates().TemplateResponse('processo.html', {'request': request, 'result': result})


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
