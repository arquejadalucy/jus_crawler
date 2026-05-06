from source.models.NumeroProcessoInfo import NumeroProcessoInfo
from source.models.ProcessoRequestBody import ProcessRequestBody


def test_numero_processo_info_derives_fields():
    processo = NumeroProcessoInfo("1234567-12.2024.1.06.1234")

    assert processo.numero_processo == "1234567-12.2024.1.06.1234"
    assert processo.numeroDigitoAnoUnificado == "1234567-12.2024"
    assert processo.tribunal == "06"


def test_process_request_body_strips_numero_processo_spaces():
    payload = ProcessRequestBody(numero_processo=" 1234567-12.2024.1.06.1234 ")

    assert payload.numero_processo == "1234567-12.2024.1.06.1234"
