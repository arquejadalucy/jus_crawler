import logging

import requests
from bs4 import BeautifulSoup

from source.models.NumeroProcessoInfo import NumeroProcessoInfo
from source.services.parse import parse_data_primeiro_grau, \
  parse_data_segundo_grau, clean_data
from source.services.tribunais_mapper import Tribunais, DominiosPorTribunal

ERROR = "ERROR"


def busca_primeiro_grau(processo: NumeroProcessoInfo, dominio: str):
    data = {"id": processo.numero_processo}
    url = (f"https://{dominio}/cpopg/search.do?conversationId=&cbPesquisa=NUMPROC"
           f"&numeroDigitoAnoUnificado={processo.numeroDigitoAnoUnificado}"
           f"&foroNumeroUnificado={processo.foro}"
           f"&dadosConsulta.valorConsultaNuUnificado={processo.numero_processo}"
           f"&dadosConsulta.valorConsultaNuUnificado=UNIFICADO&dadosConsulta.valorConsulta="
           f"&dadosConsulta.tipoNuProcesso=UNIFICADO")
    # url = f"https://{dominio}/cpopg/show.do?&processo.foro={processo.foro}" \
    #       f"&processo.numero={processo.numero_processo}"
    print(url)

    html = send_request_and_get_response(url)

    if type(html) == dict and ERROR in html:
        result = html
    else:
        result = parse_data_primeiro_grau(html)

    data.update({"Primeiro Grau": result})

    return data


def busca_codigo_segundo_grau(url: str):
    codigo = ""
    html = send_request_and_get_response(url)

    if type(html) == dict and ERROR in html:
        return ""

    elif html.find(class_='modal__lista-processos'):
        codigo = html.find(id='processoSelecionado').get('value')

    return codigo


def busca_segundo_grau(processo: NumeroProcessoInfo, dominio: str):
    data = {"id": processo.numero_processo}
    url = f"https://{dominio}/cposg5/search.do?" \
          f"cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={processo.numeroDigitoAnoUnificado}" \
          f"&foroNumeroUnificado={processo.foro}&dePesquisaNuUnificado={processo.numero_processo}" \
          f"&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"
    codigo = busca_codigo_segundo_grau(url)
    print("URL BUSCA CODIGO 2 GRAU: " + url)
    if codigo:
        url = f"https://{dominio}/cposg5/show.do?processo.codigo={codigo}"
        print("URL 2 GRAU: " + url)

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


def search_process_data(process: NumeroProcessoInfo):
    nome_tribunal = Tribunais(process.tribunal).name
    print("Nome tribunal:", nome_tribunal)
    dominio = str(DominiosPorTribunal[nome_tribunal].value)
    print("Dominio:", dominio)
    data = busca_primeiro_grau(process, dominio)
    data.update(busca_segundo_grau(process, dominio))
    print(data)
    return data
