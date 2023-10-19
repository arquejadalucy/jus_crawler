import os
import sys

import pytest

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from app import crawler
from app.models import ProcessRequestInformations
from tests.Stubs import NUMERO_PROCESSO_SEM_INFO_NO_SEGUNDO_GRAU, DOMINIO_TJAL, PROCESSO_NAO_ENCONTRADO, \
    get_url_tjal_segundo_grau, NUMERO_PROCESSO_SEM_ADVOGADOS_TJCE, DOMINIO_TJCE, NUMERO_PROCESSO_TEST_CODIGO, \
    CODIGO_PROCESSO


def test_crawler_should_search_process_with_success():
    # arrange
    processo_info = ProcessRequestInformations(NUMERO_PROCESSO_TEST_CODIGO)

    # act
    response = crawler.search_process_data(processo_info)

    # assert
    assert len(response.get('Primeiro Grau').get("movimentações")) > 0
    assert len(response.get("Primeiro Grau").get('assunto')) > 0
    assert len(response.get("Primeiro Grau").get('classe')) > 0


def test_should_return_error_when_process_info_not_found():
    # arrange
    processo_info = ProcessRequestInformations(NUMERO_PROCESSO_SEM_INFO_NO_SEGUNDO_GRAU)

    # act
    crawler_response = crawler.busca_segundo_grau(processo_info, DOMINIO_TJAL)

    # assert
    assert crawler_response.get('Segundo Grau') == {"ERROR": PROCESSO_NAO_ENCONTRADO}


@pytest.mark.skip()
def test_crawler_should_return_info_when_part_has_no_lawyer():
    """
    Deprecated: esse processo não está mais sendo encontrado na base do TJCE
    """
    # arrange
    processo_info = ProcessRequestInformations(NUMERO_PROCESSO_SEM_ADVOGADOS_TJCE)

    # act
    info_primeiro_grau = crawler.busca_primeiro_grau(processo_info, DOMINIO_TJCE)

    # assert
    assert "advogados" not in info_primeiro_grau.get('Primeiro Grau').get("partes")[0].keys()


def test_busca_segundo_grau_com_codigo():
    # arrange
    processo_info = ProcessRequestInformations(NUMERO_PROCESSO_TEST_CODIGO)
    url = get_url_tjal_segundo_grau(processo_info)
    codigo = crawler.busca_codigo_segundo_grau(url)

    # act
    response = crawler.busca_segundo_grau(processo_info, DOMINIO_TJAL)

    # assert
    assert codigo == CODIGO_PROCESSO
    assert "ERROR" not in response.get('Segundo Grau')
    assert response.get("id") == NUMERO_PROCESSO_TEST_CODIGO
    assert len(response.get('Segundo Grau').get("movimentações")) > 0
    assert response.get("Segundo Grau").get('assunto') == "Obrigações"
