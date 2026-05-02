from source.models.NumeroProcessoInfo import NumeroProcessoInfo


def test_numero_processo_info_derives_fields():
    processo = NumeroProcessoInfo("1234567-12.2024.1.06.1234")

    assert processo.numero_processo == "1234567-12.2024.1.06.1234"
    assert processo.numeroDigitoAnoUnificado == "1234567-12.2024"
    assert processo.tribunal == "06"
