from bs4 import BeautifulSoup

from source.services.parse import clean_data, get_partes, parse_data_primeiro_grau, parse_data_segundo_grau
from tests.html_stubs import HTML_PRIMEIRO_GRAU, HTML_SEGUNDO_GRAU


def test_clean_data_strips_whitespace_and_html_entities():
  assert clean_data("  texto \n\t") == "texto"


def test_get_partes_extracts_parties_and_lawyers():
    html = BeautifulSoup(HTML_PRIMEIRO_GRAU, "lxml")

    partes = get_partes(html)

    assert partes == [
        {
            "nome": "Autor",
            "tipo_de_participacao": "Parte Ativa",
            "advogados": ["Dr. Primeiro", "Dra. Segunda"],
        }
    ]


def test_get_partes_uses_fallback_table_when_primary_is_missing():
    html = BeautifulSoup(HTML_SEGUNDO_GRAU, "lxml")

    partes = get_partes(html)

    assert partes == [
        {
            "nome": "Recorrente",
            "tipo_de_participacao": "Parte Recorrente",
            "advogados": [],
        }
    ]


def test_parse_data_primeiro_grau_extracts_core_fields():
    html = BeautifulSoup(HTML_PRIMEIRO_GRAU, "lxml")

    parsed = parse_data_primeiro_grau(html)

    assert parsed["classe"] == "Classe Exemplo"
    assert parsed["area"] == "Cível"
    assert parsed["assunto"] == "Assunto Exemplo"
    assert parsed["data"] == "10/01/2024"
    assert parsed["juiz"] == "Juiz da Vara"
    assert parsed["valor"] == "R$ 1.234,56"
    assert parsed["partes"][0]["nome"] == "Autor"
    assert parsed["movimentações"][0].descricao == "Movimentação com espaços"


def test_parse_data_segundo_grau_extracts_core_fields():
    html = BeautifulSoup(HTML_SEGUNDO_GRAU, "lxml")

    parsed = parse_data_segundo_grau(html)

    assert parsed["classe"] == "Classe Recurso"
    assert parsed["area"] == "Criminal"
    assert parsed["assunto"] == "Assunto Recurso"
    assert parsed["data"] == "11/01/2024"
    assert parsed["juiz"] == "Desembargador"
    assert parsed["valor"] == "R$ 9.876,54"
    assert parsed["partes"][0]["nome"] == "Recorrente"
    assert parsed["movimentações"][0].descricao == "Distribuído ao relator"
