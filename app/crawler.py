import logging

import requests
from bs4 import BeautifulSoup

from app.enums import Tribunais, DominiosPorTribunal
from app.models import ProcessRequestInformations
from app.utils import parse_data_primeiro_grau, parse_data_segundo_grau, clean_data

ERROR = "ERROR"

PROCESSO_NAO_ENCONTRADO = "Não existem informações disponíveis para os parâmetros informados."


def busca_primeiro_grau(processo: ProcessRequestInformations, dominio: str):
    data = {"id": processo.numero_processo}
    url = f"https://{dominio}/cpopg/show.do?&processo.foro={processo.foro}" \
          f"&processo.numero={processo.numero_processo}"

    html = send_request_and_get_response(url)

    if type(html) == dict and ERROR in html:
        result = html
    else:
        result = parse_data_primeiro_grau(html)

    data.update({"Primeiro Grau": result})

    return data


def busca_codigo_segundo_grau(url: str, processo: ProcessRequestInformations):
    codigo = ""
    html = send_request_and_get_response(url)

    if type(html) == dict and ERROR in html:
        return ""

    elif html.find(class_='modal__lista-processos'):
        codigo = html.find(id='processoSelecionado').get('value')

    return codigo


def busca_segundo_grau(processo: ProcessRequestInformations, dominio: str):
    data = {"id": processo.numero_processo}
    url = f"https://{dominio}/cposg5/search.do?" \
          f"cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={processo.numeroDigitoAnoUnificado}" \
          f"&foroNumeroUnificado={processo.foro}&dePesquisaNuUnificado={processo.numero_processo}" \
          f"&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"
    codigo = busca_codigo_segundo_grau(url, processo)
    if codigo:
        url = f"https://{dominio}/cposg5/show.do?processo.codigo={codigo}"

    html = send_request_and_get_response(url)

    if type(html) == dict and ERROR in html:
        result = html
    else:
        result = parse_data_segundo_grau(html)

    data.update({"Segundo Grau": result})
    return data


def send_request_and_get_response(url):
    response = requests.get(url)
    result = BeautifulSoup(response.text, "lxml")

    if result.find(id='mensagemRetorno'):
        error = clean_data(result.find(id='mensagemRetorno').find("li").text)
        logging.error(error)
        result = {ERROR: error}
    return result


def search_process_data(process: ProcessRequestInformations):
    nome_tribunal = Tribunais(process.tribunal).name
    dominio = DominiosPorTribunal[nome_tribunal].value
    data = busca_primeiro_grau(process, dominio)
    data.update(busca_segundo_grau(process, dominio))
    return data


# if __name__ == "__main__":
#     processo = ProcessRequestInformations('0070337-91.2008.8.06.0001')
#     print(busca_primeiro_grau(processo, DominiosPorTribunal.TJCE.value))
#     print(busca_segundo_grau(processo, DominiosPorTribunal.TJCE.value))
