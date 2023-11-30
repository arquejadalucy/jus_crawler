import firebase_admin
import pyrebase
from firebase_admin import credentials
from cerberus import Validator
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from source.services.collect import search_process_data
from source.models.NumeroProcessoInfo import NumeroProcessoInfo
from source.models.ProcessoRequestBody import ProcessRequestBody
from source.services.validate import process_request_informations_schema, id_processo_schema, \
    ProcessNumberRegexErrorHandler

app = FastAPI()
validator = Validator(error_handler=ProcessNumberRegexErrorHandler)

if not firebase_admin._apps:
    cred = credentials.Certificate("/Users/lucyvelasco/PycharmProjects/jus_crawler/serviceAccount.json")
    firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyDp_XqMeP6rQ061y6M9mtlPp-JFatYBa-4",
  "authDomain": "crawler-jus.firebaseapp.com",
  "databaseURL": "https://crawler-jus-default-rtdb.firebaseio.com",
  "projectId": "crawler-jus",
  "storageBucket": "crawler-jus.appspot.com",
  "messagingSenderId": "654136178133",
  "appId": "1:654136178133:web:42658f521054817806395c",
  "measurementId": "G-QN0D2Q1SF7"
}

firebase = pyrebase.initialize_app(firebaseConfig)



def valid_request(processo_info: NumeroProcessoInfo):
    return validator.validate(processo_info.__dict__, process_request_informations_schema)


def valid_process_id(numero_processo: str):
    return validator.validate({"numero_processo": numero_processo}, id_processo_schema)


@app.post("/cadastro")
async def create_an_account():
    pass


@app.post("/login")
async def create_access_token():
    pass


@app.post("/ping")
async def validate_token():
    pass


@app.post("/processo")
def buscar_processo(process_request: ProcessRequestBody):
    """
    API que busca dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE).

    O número do processo deve seguir a estrutura de dígitos NNNNNNN-DD.AAAA.J.TR.OOOO conforme padrão do CNJ.

    Input: JSON contendo o número do processo - {"numero_processo": "string"}

    Output: JSON contendo as seguintes informações:

    * classe
    * área
    * assunto
    * data de distribuição
    * juiz
    * valor da ação
    * partes do processo
    * lista das movimentações
    \f
    :param process_request: User input
    :return:
    """
    if not valid_process_id(process_request.numero_processo):
        return validator.errors

    processo_info = NumeroProcessoInfo(process_request.numero_processo)

    if not valid_request(processo_info):
        return validator.errors

    response = search_process_data(processo_info)
    return response


@app.get("/processo/{id_processo}")
def get_processo_info_by_id(id_processo: str):
    """
    API que busca dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE).

    O número do processo deve seguir a estrutura de dígitos NNNNNNN-DD.AAAA.J.TR.OOOO conforme padrão do CNJ.

    Input: Número do processo

    Output: JSON contendo as seguintes informações:

    * classe
    * área
    * assunto
    * data de distribuição
    * juiz
    * valor da ação
    * partes do processo
    * lista das movimentações
    \f
    :param process_request: User input
    :return:
    """
    if not valid_process_id(id_processo):
        return validator.errors

    processo_info = NumeroProcessoInfo(id_processo)

    if not valid_request(processo_info):
        return validator.errors
    return search_process_data(processo_info)


def get_jinja_templates():
    app.mount("/static", StaticFiles(directory="front-end/static"), name="static")
    return Jinja2Templates(directory="front-end/templates")


@app.post('/buscaprocesso', include_in_schema=False)
def buscar_processo_pelo_form(request: Request, id_processo: str = Form()):
    result = get_processo_info_by_id(id_processo)
    return get_jinja_templates().TemplateResponse('processo.html', {'request': request, 'result': result})


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def main(request: Request):
    return get_jinja_templates().TemplateResponse('home.html', {'request': request})
