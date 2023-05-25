from app.enums import TRIBUNAIS_VALIDOS, Tribunais


def tribunal_suportado(field, value, error):
    if value not in TRIBUNAIS_VALIDOS:
        error(field, f"Tribunal não suportado. Tribunais válidos: {[tribunal.name for tribunal in Tribunais]}")


process_request_body_schema = {
    'numero_processo': {'type': 'string', 'required': True}
}

id_processo_schema = {'id': {'type': 'string',
                             'regex': "\d\d\d\d\d\d\d-\d\d\.\d\d\d\d\.\d\.\d\d\.\d\d\d\d"}}

process_request_informations_schema = {
    'numero_processo': {'type': 'string', 'required': True},
    'foro': {'type': 'string'},
    'numeroDigitoAnoUnificado': {'type': 'string'},
    'tribunal': {'type': 'string',
                 'check_with': tribunal_suportado}
}
