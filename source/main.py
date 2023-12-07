import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from source.controller.processos import get_processo_info_by_id
from source.controller import processos, users
from source.controller.users import create_access_token
from source.schemas.AuthenticationSchemas import LoginSchema

app = FastAPI()
app.include_router(users.router)
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


@app.get('/entrar', response_class=HTMLResponse, tags=["entrar"], include_in_schema=False)
def main(request: Request):
    return get_jinja_templates().TemplateResponse('entrar.html', {'request': request})


@app.post('/signin', include_in_schema=False)
def buscar_processo_pelo_form(request: Request, email: str = Form(), password: str = Form()):
    user = LoginSchema(email=email, password=password)
    result = create_access_token(user)
    return get_jinja_templates().TemplateResponse('home.html', {'request': request, 'result': result})


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
