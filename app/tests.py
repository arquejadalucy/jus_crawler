import json
from unittest import TestCase

from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


class Test(TestCase):

    def test_dados_processo(self):
        # arrange
        expected_response = {"classe": "classe1", "area": "area1", "assunto": "assunto1",
                             "data": "11/11/2011", "juiz": "José Carlos",
                             "valor": "R$1.000,00", "partes": ["Lucy", "Maria", "Netflix"],
                             "movements": {"11.11.2011": "criado",
                                           "11/01/2011": "publicado"}}

        # act
        response = client.get("/processos/1")

        # assert
        assert response.status_code == 200
        assert response.json() == expected_response

    def test_get_process_by_id(self):
        # arrange
        numero_do_processo = 1
        expected_response = main.processos.get(numero_do_processo)
        body = {"processo": numero_do_processo}

        # act
        response = client.post(
            "/processo",
            json=body,
            data=json.dumps(body))

        # assert
        print(response)
        assert response.status_code == 200
        assert response.json() == expected_response
