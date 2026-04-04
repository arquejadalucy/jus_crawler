import os
import sys

import pytest as pytest

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from fastapi.testclient import TestClient

from source.controller.processos import app
from source.services.validate import validate_process_number_message
from Stubs import get_request_body_json_test, \
    NUMERO_PROCESSO_TRIBUNAL_INVALIDO, TRIBUNAL_NAO_SUPORTADO, \
    NUMERO_PROCESSO_TEST_CODIGO, NUMERO_PROCESSO_SEM_INFO_NO_SEGUNDO_GRAU

client = TestClient(app)


@pytest.mark.parametrize(
    "invalid_number, field, error_message",
    [("1", "numero_processo", validate_process_number_message),
     (NUMERO_PROCESSO_TRIBUNAL_INVALIDO, "tribunal", TRIBUNAL_NAO_SUPORTADO)]
)
def test_return_error_when_get_request_with_invalid_field(
        invalid_number, field, error_message):
    # arrange
    def get_message_from_response(message):
        return {True: message[0],
                False: message}[isinstance(message, list)]

    # act
    response = client.get(f"/processo/{invalid_number}")

    # assert
    assert response is not None
    assert len(response.json()) == 1
    assert len(response.json().get(field)) == 1
    assert error_message in get_message_from_response(
        response.json().get(field))


@pytest.mark.parametrize(
    "invalid_number, field, error_message",
    [("500", "numero_processo", validate_process_number_message),
     ("", "numero_processo", validate_process_number_message),
     (NUMERO_PROCESSO_TRIBUNAL_INVALIDO, "tribunal", TRIBUNAL_NAO_SUPORTADO)]
)
def test_return_error_when_post_request_with_invalid_field(
        invalid_number, field, error_message):
    # arrange
    def get_message_from_response(message):
        return {True: message[0],
                False: message}[isinstance(message, list)]

    # act
    response = client.post(
        "/processo",
        json=get_request_body_json_test(invalid_number))

    # assert
    assert response is not None
    assert len(response.json()) == 1
    assert len(response.json().get(field)) == 1
    assert error_message in get_message_from_response(
        response.json().get(field))


@pytest.mark.parametrize(
    "cnj, expected_in_segundo_grau",
    [(NUMERO_PROCESSO_TEST_CODIGO, "movimentações"),
     (NUMERO_PROCESSO_SEM_INFO_NO_SEGUNDO_GRAU, "ERROR")]
)
def test_return_success_when_post_request(
        cnj, expected_in_segundo_grau):
    # arrange

    # act
    response = client.post(
        "/processo",
        json=get_request_body_json_test(cnj))

    # assert
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 3
    assert cnj == response.get("id")
    assert len(response.get('Primeiro Grau').get("movimentações")) > 0
    assert expected_in_segundo_grau in response.get('Segundo Grau')
    assert len(response.get('Segundo Grau').get(expected_in_segundo_grau)) > 0


@pytest.mark.parametrize(
    "cnj, expected_in_segundo_grau",
    [(NUMERO_PROCESSO_TEST_CODIGO, "movimentações"),
     (NUMERO_PROCESSO_SEM_INFO_NO_SEGUNDO_GRAU, "ERROR")]
)
def test_return_success_when_get_request(
        cnj, expected_in_segundo_grau):
    # arrange

    # act
    response = client.get(f"/processo/{cnj}")

    # assert
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 3
    assert cnj == response.get("id")
    assert len(response.get('Primeiro Grau').get("movimentações")) > 0
    assert expected_in_segundo_grau in response.get('Segundo Grau')
    assert len(response.get('Segundo Grau').get(expected_in_segundo_grau)) > 0
