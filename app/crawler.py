import logging

import requests
from bs4 import BeautifulSoup

from app.enums import TRIBUNAIS_VALIDOS, Tribunais, DominiosPorTribunal
from app.exceptions import TribunalInvalidoException, ProcessCodeNotFoundException
from models import ProcessRequestInformations
from utils import parse_data_primeiro_grau, parse_data_segundo_grau, clean_data

PROCESSO_NAO_ENCONTRADO = "Não existem informações disponíveis para os parâmetros informados."


def busca_primeiro_grau(processo: ProcessRequestInformations, dominio: str):
    data = {"id": processo.numero_processo}
    url = f"https://{dominio}/cpopg/show.do?&processo.foro={processo.foro}" \
          f"&processo.numero={processo.numero_processo}"

    html = send_request_and_get_response(url)

    result = {}

    if html.find(id='numeroProcesso') is not None:
        result = parse_data_primeiro_grau(html)

    elif html.find(id='mensagemRetorno') is not None:
        error = clean_data(html.find(id='mensagemRetorno').find("li").text)
        logging.error(error)
        result = {"ERROR": error}

    data.update({"Primeiro Grau": result})

    return data


def busca_codigo_segundo_grau(processo: ProcessRequestInformations, dominio: str):
    url = f"https://{dominio}/cposg5/search.do?conversationId=&paginaConsulta=0" \
          f"&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={processo.numeroDigitoAnoUnificado}" \
          f"&foroNumeroUnificado={processo.foro}&dePesquisaNuUnificado={processo.numero_processo}" \
          f"&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"

    html = send_request_and_get_response(url)

    if html.find(class_='modal__lista-processos') is None:
        raise ProcessCodeNotFoundException

    codigo = html.find(id='processoSelecionado').get('value')
    return codigo


def busca_segundo_grau(processo: ProcessRequestInformations, dominio: str):
    data = {"id": processo.numero_processo}
    result = {}
    try:
        codigo = busca_codigo_segundo_grau(processo, dominio)
        url = f"https://{dominio}/cposg5/show.do?processo.codigo={codigo}"
        html = send_request_and_get_response(url)
        result = parse_data_segundo_grau(html)

    except ProcessCodeNotFoundException as e:
        result = PROCESSO_NAO_ENCONTRADO

    data.update({"Segundo Grau": result})
    return data


def send_request_and_get_response(url):
    response = requests.get(url)
    html = BeautifulSoup(response.text, "lxml")
    return html


def validate_info(process: ProcessRequestInformations):
    if process.tribunal not in TRIBUNAIS_VALIDOS:
        raise TribunalInvalidoException


def search_process_data(process: ProcessRequestInformations):
    validate_info(process)
    nome_tribunal = Tribunais(process.tribunal).name
    dominio = DominiosPorTribunal[nome_tribunal].value
    data = busca_primeiro_grau(process, dominio)
    data.update(busca_segundo_grau(process, dominio))
    return data


if __name__ == "__main__":
    processo = ProcessRequestInformations('0710802-55.2018.8.02.0001')
    print(busca_primeiro_grau(processo, DominiosPorTribunal.TJAL.value))
    print(busca_segundo_grau(processo, DominiosPorTribunal.TJAL.value))
