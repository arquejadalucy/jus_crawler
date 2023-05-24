import os
import sys

from app.crawler import send_request_and_get_response

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from unittest import TestCase
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app import crawler
from app.api import app
from app.models import ProcessRequestInformations
from Stubs import expected_response_body, request_body_json_test, NUMERO_PROCESSO_TEST, PROCESSO_NAO_ENCONTRADO, \
    NUMERO_PROCESSO_TEST_CODIGO, DOMINIO_TJAL, CODIGO_PROCESSO, get_url_tjal_segundo_grau

client = TestClient(app)


class ApiTests(TestCase):

    def test_client_should_retrieve_with_success_when_post_request(self):
        # arrange
        # act
        response = client.post(
            "/processo",
            json=request_body_json_test)

        # assert
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert len(response.json().get('Primeiro Grau').get("movimentações")) > 0
        assert len(response.json().get('Segundo Grau').get("movimentações")) > 0
        assert response.json().get("Primeiro Grau").get("juiz") == expected_response_body.get("Primeiro Grau").get("juiz")

    def test_client_should_retrieve_with_success_when_get_request(self):
        # arrange
        # act
        response = client.get(f"/processo/{NUMERO_PROCESSO_TEST}")

        # assert
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert "ERROR" not in response.json().get('Segundo Grau')
        assert len(response.json().get('Primeiro Grau').get("movimentações")) > 0
        assert len(response.json().get('Segundo Grau').get("movimentações")) > 0
        assert response.json().get("Primeiro Grau").get("juiz") == expected_response_body.get("Primeiro Grau").get("juiz")

    def test_crawler_deve_buscar_processo_com_sucesso(self):
        # arrange
        processo_info = ProcessRequestInformations(NUMERO_PROCESSO_TEST)

        # act
        process_data = crawler.search_process_data(processo_info)

        # assert
        assert process_data == expected_response_body
        assert process_data.keys() == expected_response_body.keys()

    def test_crawler_search_second_when_process_info_not_found(self):
        # arrange
        numero_processo = "0022301-24.2011.8.02.0001"
        dominio = "www2.tjal.jus.br"

        # act
        response = crawler.busca_segundo_grau(ProcessRequestInformations(numero_processo), dominio)

        # assert
        assert response.get('Segundo Grau') == {"ERROR": PROCESSO_NAO_ENCONTRADO}

    def test_crawler_search_first_when_process_info_not_found(self):
        # arrange
        numero_processo = "0022301-24.2011.8.02.0001"
        processo_info = ProcessRequestInformations(numero_processo)
        url = get_url_tjal_segundo_grau(processo_info)

        mock_html = send_request_and_get_response(url)
        crawler.send_request_and_get_response = MagicMock(return_value=mock_html)

        # act
        response = crawler.busca_primeiro_grau(ProcessRequestInformations(numero_processo), dominio)

        # assert
        assert response.get('Primeiro Grau') == {"ERROR": PROCESSO_NAO_ENCONTRADO}

    def test_busca_segundo_grau_com_codigo(self):
        # arrange
        processo_info = ProcessRequestInformations(NUMERO_PROCESSO_TEST_CODIGO)
        url = get_url_tjal_segundo_grau(processo_info)
        codigo = crawler.busca_codigo_segundo_grau(url, processo_info)

        # act
        response = crawler.busca_segundo_grau(processo_info, DOMINIO_TJAL)

        # assert
        assert codigo == CODIGO_PROCESSO
        assert "ERROR" not in response.get('Segundo Grau')
        assert len(response.get('Segundo Grau').get("movimentações")) > 0
