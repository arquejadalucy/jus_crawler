from cerberus import Validator
from fastapi import APIRouter, HTTPException
import logging
from time import perf_counter
from source.services.collect import search_process_data
from source.models.NumeroProcessoInfo import NumeroProcessoInfo
from source.models.ProcessoRequestBody import ProcessRequestBody
from source.services.validate import process_request_informations_schema, id_processo_schema, \
    ProcessNumberRegexErrorHandler


router = APIRouter(
    prefix="/processos",
    tags=["processos"]
)

validator = Validator(error_handler=ProcessNumberRegexErrorHandler)


def normalize_numero_processo(numero_processo: str):
    if isinstance(numero_processo, str):
        return numero_processo.strip()
    return numero_processo


def valid_request(processo_info: NumeroProcessoInfo):
    return validator.validate(processo_info.__dict__, process_request_informations_schema)


def valid_process_id(numero_processo: str):
    numero_processo = normalize_numero_processo(numero_processo)
    return validator.validate({"numero_processo": numero_processo}, id_processo_schema)


def fetch_processo_info(id_processo: str):
    """Core lookup used by both endpoint and background tasks.

    Raises ValueError on validation errors with the `validator.errors` payload.
    Returns the result of `search_process_data` on success.
    """
    id_processo = normalize_numero_processo(id_processo)
    if not valid_process_id(id_processo):
        raise ValueError(validator.errors)

    processo_info = NumeroProcessoInfo(id_processo)

    if not valid_request(processo_info):
        raise ValueError(validator.errors)

    payload = search_process_data(processo_info)

    return payload


@router.post("/busca")
def buscar_processo(process_request: ProcessRequestBody):
    """
    API que busca dados de um processo em todos os graus dos
    Tribunais de Justiça de Alagoas (TJAL), do Ceará (TJCE) e de São Paulo (TJSP).

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
    started_at = perf_counter()
    try:
        result = fetch_processo_info(process_request.numero_processo)
        elapsed_seconds = perf_counter() - started_at
        logging.getLogger(__name__).info(
            "Process search API executed in %.4fs for numero_processo=%s",
            elapsed_seconds,
            process_request.numero_processo,
        )
        return result
    except ValueError as exc:
        elapsed_seconds = perf_counter() - started_at
        logging.getLogger(__name__).info(
            "Process search API failed in %.4fs for numero_processo=%s",
            elapsed_seconds,
            process_request.numero_processo,
        )
        raise HTTPException(status_code=400, detail=exc.args[0])


@router.get("/{id_processo}")
def get_processo_info_by_id(id_processo: str):
    """
    API que busca dados de um processo em todos os graus dos
    Tribunais de Justiça de Alagoas (TJAL), do Ceará (TJCE) e de São Paulo (TJSP).

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
    started_at = perf_counter()
    try:
        logging.getLogger(__name__).debug("Fetching processo info for id %s", id_processo)
        result = fetch_processo_info(id_processo)
        elapsed_seconds = perf_counter() - started_at
        logging.getLogger(__name__).info(
            "Process search API executed in %.4fs for id_processo=%s",
            elapsed_seconds,
            id_processo,
        )
        return result
    except ValueError as exc:
        elapsed_seconds = perf_counter() - started_at
        logging.getLogger(__name__).info(
            "Process search API failed in %.4fs for id_processo=%s",
            elapsed_seconds,
            id_processo,
        )
        raise HTTPException(status_code=400, detail=exc.args[0])
