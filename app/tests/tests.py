import json
from unittest import TestCase
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app import crawler
from app.api import app
from app.tests.Stubs import expected_response_body, NUMERO_PROCESSO_TEST, request_body_test

client = TestClient(app)


class Test(TestCase):

    def test_buscar_processo(self):
        # arrange
        crawler.search_process_data = MagicMock(return_value=expected_response_body)

        # act
        response = client.post(
            "/processo",
            json=request_body_test)

        # assert
        assert response.status_code == 200
        assert response.json() == expected_response_body