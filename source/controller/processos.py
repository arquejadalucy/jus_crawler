from cerberus import Validator
from fastapi import APIRouter
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


def valid_request(processo_info: NumeroProcessoInfo):
    return validator.validate(processo_info.__dict__, process_request_informations_schema)


def valid_process_id(numero_processo: str):
    return validator.validate({"numero_processo": numero_processo}, id_processo_schema)


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
    if not valid_process_id(process_request.numero_processo):
        return validator.errors

    processo_info = NumeroProcessoInfo(process_request.numero_processo)

    if not valid_request(processo_info):
        return validator.errors

    response = search_process_data(processo_info)
    return response


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
    if not valid_process_id(id_processo):
        return validator.errors

    processo_info = NumeroProcessoInfo(id_processo)

    if not valid_request(processo_info):
        return validator.errors
    return search_process_data(processo_info)
