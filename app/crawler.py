import requests
from bs4 import BeautifulSoup

from app.utils import extract_info_from_process_number


def parse_data():
    pass


def busca_primeiro_grau(numero_processo: str, foro: str):
    data = {"id": numero_processo}
    url=f"https://www2.tjal.jus.br/cpopg/show.do?" \
          f"&processo.foro={foro}&processo.numero={numero_processo}"

    response = requests.get(url)

    html = BeautifulSoup(response.text, "html.parser")

    parsed_data = parse_data()

    data.update({"Primeiro Grau": parsed_data})
    return data


def parse_data_segundo_grau(html):
    if bool(html.find(class_='modal__lista-processos')):
        codigo = html.find_all(class_='.modal__lista-processos__item__header #processoSelecionado')[0].split(" ")[-1] \
            .replace('value="', "").replace('">', "")
        url2 = f"https://www2.tjal.jus.br/cposg5/show.do?processo.codigo={codigo}"

        response = requests.get(url2)
        process_html = BeautifulSoup(response.text, "html.parser")

        data = parse_data()
        return data



def busca_segundo_grau(numero_processo: str, foro: str, numeroDigitoAnoUnificado: str):
    data = {"id": numero_processo}
    url = f"https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0" \
                   f"&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={numeroDigitoAnoUnificado}" \
                   f"&foroNumeroUnificado={foro}&dePesquisaNuUnificado={numero_processo}" \
                   f"&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"

    response = requests.get(url)

    html = BeautifulSoup(response.text, "html.parser")

    parsed_data = parse_data_segundo_grau(html)

    data.update({"Segundo Grau": parsed_data})
    return data


