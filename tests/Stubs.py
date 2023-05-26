from app.enums import DominiosPorTribunal
from app.models import ProcessRequestInformations

TRIBUNAL_NAO_SUPORTADO = "Tribunal não suportado."

CLASSE_PROCESSO_TESTE_PRIMEIRO_GRAU = "Procedimento Comum Cível"
CLASSE_PROCESSO_TESTE_SEGUNDO_GRAU = "Apelação Cível"
ASSUNTO_PROCESSO_TESTE_PRIMEIRO_GRAU = "Planos de Saúde"
ASSUNTO_PROCESSO_TESTE_SEGUNDO_GRAU = "Fornecimento de medicamentos"

PROCESSO_NAO_ENCONTRADO = "Não existem informações disponíveis para os parâmetros informados."

DOMINIO_TJAL = str(DominiosPorTribunal.TJAL.value)
DOMINIO_TJCE = str(DominiosPorTribunal.TJCE.value)
NUMERO_PROCESSO_TEST_CENARIO_SUCESSO = "0165801-59.2019.8.06.0001"
NUMERO_PROCESSO_SEM_INFO_NO_SEGUNDO_GRAU = "0022301-24.2011.8.02.0001"
NUMERO_PROCESSO_TEST_CODIGO = "0710802-55.2018.8.02.0001"
NUMERO_PROCESSO_SEM_ADVOGADOS = "0070337-91.2008.8.06.0001"
NUMERO_PROCESSO_TRIBUNAL_INVALIDO = "0070337-91.2008.8.04.0001"
CODIGO_PROCESSO = "P00006BXP0000"


def get_request_body_json_test(numero_processo: str):
    return {"numero_processo": numero_processo}


def get_url_tjal_segundo_grau(processo_info: ProcessRequestInformations):
    return f"https://{DOMINIO_TJAL}/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC" \
           f"&numeroDigitoAnoUnificado={processo_info.numeroDigitoAnoUnificado}" \
           f"&foroNumeroUnificado={processo_info.foro}&dePesquisaNuUnificado={processo_info.numero_processo}" \
           f"&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"
