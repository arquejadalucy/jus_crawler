from abc import ABC

from cerberus import errors

from source.services.tribunais_mapper import TRIBUNAIS_VALIDOS, Tribunais

validate_process_number_message = "ERROR: Número do processo deve seguir a estrutura de dígitos " \
                                  "NNNNNNN-DD.AAAA.J.TR.OOOO conforme padrão do CNJ."


class ProcessNumberRegexErrorHandler(errors.BasicErrorHandler, ABC):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REGEX_MISMATCH.code] = validate_process_number_message


def tribunal_suportado(field, value, error):
    if value not in TRIBUNAIS_VALIDOS:
        error(field, f"ERROR: Tribunal não suportado. Tribunais válidos: {[tribunal.name for tribunal in Tribunais]}")


numero_processo_rules = {'type': 'string',
                         'required': True,
                         'regex': "\d\d\d\d\d\d\d-\d\d\.\d\d\d\d\.\d\.\d\d\.\d\d\d\d"}

id_processo_schema = {'numero_processo': numero_processo_rules}

process_request_informations_schema = {
    'numero_processo': numero_processo_rules,
    'foro': {'type': 'string'},
    'numeroDigitoAnoUnificado': {'type': 'string'},
    'tribunal': {'type': 'string',
                 'check_with': tribunal_suportado}
}
