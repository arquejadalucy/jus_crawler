from source.models.NumeroProcessoInfo import NumeroProcessoInfo
from source.services import collect


class FakeResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code


def test_search_process_data_filters_invalid_sections_and_keeps_errors(monkeypatch):
    processo = NumeroProcessoInfo("1234567-12.2024.1.06.1234")

    monkeypatch.setattr(
        collect,
        "busca_primeiro_grau",
        lambda process, dominio: {
            "id": process.numero_processo,
            "Primeiro Grau": {"area": "Cível"},
        },
    )
    monkeypatch.setattr(
        collect,
        "busca_segundo_grau",
        lambda process, dominio: {
            "id": process.numero_processo,
            "Segundo Grau": {"ERROR": "consulta indisponível"},
        },
    )

    resultado = collect.search_process_data(processo)

    assert resultado == {
        "id": "1234567-12.2024.1.06.1234",
        "tribunal": "TJCE",
        "Segundo Grau": {"ERROR": "consulta indisponível"},
    }


def test_send_request_and_get_response_uses_timeout_and_retries(monkeypatch):
    calls = []

    def fake_get(url, timeout):
        calls.append((url, timeout))
        if len(calls) < 3:
            raise collect.requests.RequestException("temporary failure")
        return FakeResponse("<html><body><div>ok</div></body></html>")

    monkeypatch.setattr(collect.requests, "get", fake_get)
    monkeypatch.setattr(collect.time, "sleep", lambda seconds: None)

    result = collect.send_request_and_get_response("https://example.test/processo")

    assert result.find("div").text == "ok"
    assert len(calls) == collect.REQUEST_RETRIES
    assert all(timeout == collect.REQUEST_TIMEOUT_SECONDS for _, timeout in calls)


def test_send_request_and_get_response_returns_error_after_retries(monkeypatch):
    calls = []

    def fake_get(url, timeout):
        calls.append((url, timeout))
        raise collect.requests.RequestException("still failing")

    monkeypatch.setattr(collect.requests, "get", fake_get)
    monkeypatch.setattr(collect.time, "sleep", lambda seconds: None)

    result = collect.send_request_and_get_response("https://example.test/processo")

    assert result == {"ERROR": "still failing"}
    assert len(calls) == collect.REQUEST_RETRIES
