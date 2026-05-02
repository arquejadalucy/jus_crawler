from source.controller.processos import valid_process_id, valid_request
from source.models.NumeroProcessoInfo import NumeroProcessoInfo


def test_valid_process_id_accepts_cnj_format():
    assert valid_process_id("1234567-12.2024.1.06.1234") is True


def test_valid_process_id_rejects_invalid_format():
    assert valid_process_id("1234") is False


def test_valid_request_rejects_unsupported_tribunal():
    processo_info = NumeroProcessoInfo("1234567-12.2024.1.99.1234")

    assert valid_request(processo_info) is False
