import os
import sys

from app.crawler import send_request_and_get_response

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from unittest import TestCase
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app import crawler
from app.api import app
from app.models import ProcessRequestInformations
from Stubs import NUMERO_PROCESSO_TEST_CENARIO_SUCESSO, PROCESSO_NAO_ENCONTRADO, \
    NUMERO_PROCESSO_TEST_CODIGO, DOMINIO_TJAL, CODIGO_PROCESSO, get_url_tjal_segundo_grau, \
    NUMERO_PROCESSO_SEM_ADVOGADOS, DOMINIO_TJCE, ASSUNTO_PROCESSO_TESTE_PRIMEIRO_GRAU, \
    ASSUNTO_PROCESSO_TESTE_SEGUNDO_GRAU, CLASSE_PROCESSO_TESTE_PRIMEIRO_GRAU, CLASSE_PROCESSO_TESTE_SEGUNDO_GRAU, \
    get_request_body_json_test, NUMERO_PROCESSO_SEM_INFO_NO_SEGUNDO_GRAU, VALUE_DOES_NOT_MATCH_REGEX, \
    NUMERO_PROCESSO_TRIBUNAL_INVALIDO, TRIBUNAL_NAO_SUPORTADO

client = TestClient(app)


class ApiTests(TestCase):

    def test_client_should_retrieve_with_success_when_post_request(self):
        # arrange
        # act
        response = client.post(
            "/processo",
            json=get_request_body_json_test(NUMERO_PROCESSO_TEST_CENARIO_SUCESSO))

        # assert
        assert response.status_code == 200
        assert len(response.json()) == 3
        asserts_info_primeiro_grau_cenario_sucesso(response.json())
        asserts_info_segundo_grau_cenario_sucesso(response.json())

    def test_client_should_retrieve_with_success_when_get_request(self):
        # arrange
        # act
        response = client.get(f"/processo/{NUMERO_PROCESSO_TEST_CENARIO_SUCESSO}")

        # assert
        assert response.status_code == 200
        assert len(response.json()) == 3
        asserts_info_primeiro_grau_cenario_sucesso(response.json())
        asserts_info_segundo_grau_cenario_sucesso(response.json())

    def test_client_should_return_error_when_get_request_with_invalid_number(self):
        # arrange
        # act
        response = client.get("/processo/1")

        # assert
        assert response is not None
        assert len(response.json()) == 1
        assert len(response.json().get("id")) == 1
        assert VALUE_DOES_NOT_MATCH_REGEX in response.json().get("id")[0]

    def test_client_should_return_error_when_post_request_with_invalid_number(self):
        # arrange
        # act
        response = client.post(
            "/processo",
            json=get_request_body_json_test("500"))

        # assert
        assert response is not None
        assert len(response.json()) == 1
        assert len(response.json().get("id")) == 1
        assert VALUE_DOES_NOT_MATCH_REGEX in response.json().get("id")[0]

    def test_client_should_return_error_when_post_request_with_null_number(self):
        # arrange
        # act
        response = client.post(
            "/processo",
            json=get_request_body_json_test(""))

        # assert
        assert response is not None
        assert len(response.json()) == 1
        assert len(response.json().get("id")) == 1
        assert VALUE_DOES_NOT_MATCH_REGEX in response.json().get("id")[0]

    def test_client_should_return_error_when_post_request_with_invalid_tribunal(self):
        # arrange
        # act
        response = client.post(
            "/processo",
            json=get_request_body_json_test(NUMERO_PROCESSO_TRIBUNAL_INVALIDO))

        # assert
        assert response is not None
        assert len(response.json()) == 1
        assert len(response.json().get("tribunal")) == 1
        assert TRIBUNAL_NAO_SUPORTADO in response.json().get("tribunal")[0]

    def test_client_should_return_error_when_get_request_with_invalid_tribunal(self):
        # arrange
        # act
        response = client.get(f"/processo/{NUMERO_PROCESSO_TRIBUNAL_INVALIDO}")

        # assert
        assert response is not None
        assert len(response.json()) == 1
        assert len(response.json().get("tribunal")) == 1
        assert TRIBUNAL_NAO_SUPORTADO in response.json().get("tribunal")[0]


class CrawlerTests(TestCase):
    def test_crawler_should_search_process_with_success(self):
        # arrange
        processo_info = ProcessRequestInformations(NUMERO_PROCESSO_TEST_CENARIO_SUCESSO)

        # act
        process_data = crawler.search_process_data(processo_info)

        # assert
        asserts_info_primeiro_grau_cenario_sucesso(process_data)
        asserts_info_segundo_grau_cenario_sucesso(process_data)

    def test_second_crawler_should_return_error_when_process_info_not_found(self):
        # arrange
        processo_info = ProcessRequestInformations(NUMERO_PROCESSO_SEM_INFO_NO_SEGUNDO_GRAU)

        # act
        info_segundo_grau = crawler.busca_segundo_grau(processo_info, DOMINIO_TJAL)

        # assert
        assert info_segundo_grau.get('Segundo Grau') == {"ERROR": PROCESSO_NAO_ENCONTRADO}

    def test_first_crawler_should_return_error_when_process_info_not_found(self):
        # arrange
        processo_info = ProcessRequestInformations(NUMERO_PROCESSO_SEM_INFO_NO_SEGUNDO_GRAU)
        url = get_url_tjal_segundo_grau(processo_info)
        mock_html = send_request_and_get_response(url)

        # act
        with patch('app.crawler.send_request_and_get_response', MagicMock(return_value=mock_html)):
            info_primeiro_grau = crawler.busca_primeiro_grau(processo_info, DOMINIO_TJAL)

        # assert
        assert info_primeiro_grau.get('Primeiro Grau') == {"ERROR": PROCESSO_NAO_ENCONTRADO}

    def test_crawler_should_return_info_when_part_has_no_lawyer(self):
        # arrange
        processo_info = ProcessRequestInformations(NUMERO_PROCESSO_SEM_ADVOGADOS)

        # act
        info_primeiro_grau = crawler.busca_primeiro_grau(processo_info, DOMINIO_TJCE)

        # assert
        assert "advogados" not in info_primeiro_grau.get('Primeiro Grau').get("partes")[0].keys()

    def test_busca_segundo_grau_com_codigo(self):
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


def asserts_info_primeiro_grau_cenario_sucesso(response):
    assert len(response.get('Primeiro Grau').get("movimentações")) > 0
    assert response.get("Primeiro Grau").get('assunto') == ASSUNTO_PROCESSO_TESTE_PRIMEIRO_GRAU
    assert response.get("Primeiro Grau").get('classe') == CLASSE_PROCESSO_TESTE_PRIMEIRO_GRAU


def asserts_info_segundo_grau_cenario_sucesso(response):
    assert "ERROR" not in response.get('Segundo Grau')
    assert len(response.get('Segundo Grau').get("movimentações")) > 0
    assert response.get("Segundo Grau").get('assunto') == ASSUNTO_PROCESSO_TESTE_SEGUNDO_GRAU
    assert response.get("Segundo Grau").get('classe') == CLASSE_PROCESSO_TESTE_SEGUNDO_GRAU
