
from app.enums import TRIBUNAIS_VALIDOS

process_request_body_schema = {
    'numero_processo': {'type': 'string', 'required': True}
}


def tribunal_suportado(field, value, error):
    if value not in TRIBUNAIS_VALIDOS:
        error(field, "Tribunal não suportado.")


process_request_informations_schema = {
    'numero_processo': {'type': 'string', 'required': True},
    'foro': {'type': 'string'},
    'numeroDigitoAnoUnificado': {'type': 'string'},
    'tribunal': {'type': 'string',
                 'check_with': tribunal_suportado}
}

process_response_payload_schema = {
    "id": {'type': 'string'},
    "Primeiro Grau": {
        "classe": {'type': 'string'},
        "area": {'type': 'string'},
        "assunto": {'type': 'string'},
        "data": {'type': 'string'},
        "juiz": {'type': 'string'},
        "valor": {'type': 'string'},
        "partes": {'type': 'list',
                   'items': [{
                            'nome': {'type': 'string'},
                            'tipo_de_participacao': {'type': 'string'},
                            'advogados': {'type': 'list', 'required': False}
                   }]},
        "movimentações": {'type': 'list',
                   'items': [{
                            'data_movimentação': {'type': 'string'},
                            'descrição_movimentação': {'type': 'string'}
                   }]},
    },
    "Segundo Grau": {
        "classe": {'type': 'string'},
        "area": {'type': 'string'},
        "assunto": {'type': 'string'},
        "data": {'type': 'string'},
        "juiz": {'type': 'string'},
        "valor": {'type': 'string'},
        "partes": {'type': 'list',
                   'items': [{
                            'nome': {'type': 'string'},
                            'tipo_de_participacao': {'type': 'string'},
                            'advogados': {'type': 'list', 'required': False}
                   }]},
        "movimentações": {'type': 'list',
                   'items': [{
                            'data_movimentação': {'type': 'string'},
                            'descrição_movimentação': {'type': 'string'}
                   }]},
    }
}
