import requests
from bs4 import BeautifulSoup

from models import ProcessRequestInformations
from utils import parse_data_primeiro_grau, parse_data_segundo_grau


def busca_primeiro_grau(processo: ProcessRequestInformations):
    data = {"id": processo.numero_processo}
    url = f"https://www2.tjal.jus.br/cpopg/show.do?&processo.foro={processo.foro}" \
          f"&processo.numero={processo.numero_processo}"

    html = send_request_and_get_response(url)

    parsed_data = parse_data_primeiro_grau(html)

    data.update({"Primeiro Grau": parsed_data})

    return data


def busca_codigo_segundo_grau(processo: ProcessRequestInformations):
    url = f"https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0" \
          f"&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={processo.numeroDigitoAnoUnificado}" \
          f"&foroNumeroUnificado={processo.foro}&dePesquisaNuUnificado={processo.numero_processo}" \
          f"&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"

    html = send_request_and_get_response(url)

    if bool(html.find(class_='modal__lista-processos')):
        codigo = html.find(id='processoSelecionado').get('value')

        return codigo
    return ""


def busca_segundo_grau(processo: ProcessRequestInformations):
    data = {"id": processo.numero_processo}
    codigo = busca_codigo_segundo_grau(processo)

    url = f"https://www2.tjal.jus.br/cposg5/show.do?processo.codigo={codigo}"

    html = send_request_and_get_response(url)
    parsed_data = parse_data_segundo_grau(html)

    data.update({"Segundo Grau": parsed_data})
    return data


def send_request_and_get_response(url):
    response = requests.get(url)
    html = BeautifulSoup(response.text, "lxml")
    return html


def search_process_data(process: ProcessRequestInformations):
    data = busca_primeiro_grau(process)
    data.update(busca_segundo_grau(process))
    return data

if __name__ == "__main__":
    processo = ProcessRequestInformations('0710802-55.2018.8.02.0001')
    print(busca_primeiro_grau(processo))
    print(busca_segundo_grau(processo))
