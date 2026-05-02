import logging
import time

import requests
from bs4 import BeautifulSoup

from source.models.NumeroProcessoInfo import NumeroProcessoInfo
from source.services.parse import parse_data_primeiro_grau, \
  parse_data_segundo_grau, clean_data
from source.services.tribunais_mapper import Tribunais, DominiosPorTribunal

ERROR = "ERROR"
REQUEST_TIMEOUT_SECONDS = 30
REQUEST_RETRIES = 3
REQUEST_RETRY_DELAY_SECONDS = 1

logger = logging.getLogger(__name__)


def busca_primeiro_grau(processo: NumeroProcessoInfo, dominio: str):
    data = {"id": processo.numero_processo}
    url = (f"https://{dominio}/cpopg/search.do?conversationId=&cbPesquisa=NUMPROC"
           f"&numeroDigitoAnoUnificado={processo.numeroDigitoAnoUnificado}"
           f"&foroNumeroUnificado={processo.foro}"
           f"&dadosConsulta.valorConsultaNuUnificado={processo.numero_processo}"
           f"&dadosConsulta.valorConsultaNuUnificado=UNIFICADO&dadosConsulta.valorConsulta="
           f"&dadosConsulta.tipoNuProcesso=UNIFICADO")
    logger.debug("Consultando processo de primeiro grau", extra={"url": url, "processo_id": processo.numero_processo})

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
    logger.debug("Consultando busca de código do segundo grau", extra={"url": url, "processo_id": processo.numero_processo})
    if codigo:
        url = f"https://{dominio}/cposg5/show.do?processo.codigo={codigo}"
        logger.debug("Consultando detalhe do segundo grau", extra={"url": url, "processo_id": processo.numero_processo, "codigo": codigo})

    html = send_request_and_get_response(url)

    if type(html) == dict and ERROR in html:
        result = html
    else:
        result = parse_data_segundo_grau(html)

    data.update({"Segundo Grau": result})
    return data


def send_request_and_get_response(url):
    last_error = None

    for attempt in range(1, REQUEST_RETRIES + 1):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)

            if response.status_code >= 500:
                last_error = f"HTTP {response.status_code}"
                logger.warning(
                    "Falha transitória na consulta",
                    extra={"url": url, "attempt": attempt, "max_attempts": REQUEST_RETRIES, "status_code": response.status_code},
                )
                if attempt < REQUEST_RETRIES:
                    time.sleep(REQUEST_RETRY_DELAY_SECONDS)
                continue

            result = BeautifulSoup(response.text, "lxml")

            if result.find(id='mensagemRetorno'):
                error = clean_data(result.find(id='mensagemRetorno').find("li").text)
                logger.error(error)
                return {ERROR: error}

            return result

        except requests.RequestException as exc:
            last_error = str(exc)
            logger.warning(
                "Erro ao consultar processo",
                extra={"url": url, "attempt": attempt, "max_attempts": REQUEST_RETRIES},
                exc_info=True,
            )
            if attempt < REQUEST_RETRIES:
                time.sleep(REQUEST_RETRY_DELAY_SECONDS)

    logger.error(
        "Falha ao consultar processo após tentativas",
        extra={"url": url, "max_attempts": REQUEST_RETRIES, "last_error": last_error},
    )
    return {ERROR: last_error or "Falha ao consultar o processo"}


def search_process_data(process: NumeroProcessoInfo):
    nome_tribunal = Tribunais(process.tribunal).name
    logger.info("Tribunal identificado", extra={"tribunal": nome_tribunal, "processo_id": process.numero_processo})
    dominio = str(DominiosPorTribunal[nome_tribunal].value)
    logger.info("Domínio selecionado", extra={"dominio": dominio, "processo_id": process.numero_processo})
    data = busca_primeiro_grau(process, dominio)
    data.update(busca_segundo_grau(process, dominio))
    logger.debug("Dados brutos coletados", extra={"processo_id": process.numero_processo, "data": data})
    
    # Filtrar apenas graus com dados válidos
    filtered_data = {"id": data.get("id")}
    for grau, grau_data in data.items():
        if grau != "id":
            # Verificar se há dados válidos (não é erro e possui campo classe)
            if isinstance(grau_data, dict) and not (ERROR in grau_data) and grau_data.get("classe"):
                filtered_data[grau] = grau_data
            elif isinstance(grau_data, dict) and ERROR in grau_data:
                # Se for erro, manter para exibição da mensagem de erro
                filtered_data[grau] = grau_data
    
    return filtered_data
