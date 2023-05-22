import logging
import re


def extract_info_from_process_number(numero_processo: str):
    infos = numero_processo.split(".")
    return {"foro": numero_processo[-1],
            "numeroDigitoAnoUnificado": infos[0] + "." + infos[1]}


def get_area_processo(response):
    return response.css('#areaProcesso span::text').get()


def get_movimentos_primeiro_grau(response):
    movimentos_list = []
    movimentos = response.css('.containerMovimentacao')
    for movimento in movimentos:
        data_movimento = clean_data(movimento.css('.dataMovimentacao::text').get())
        descricao_movimento = clean_data(movimento.css('.descricaoMovimentacao::text').get())

        movimentos_list.append({"data_movimentação": data_movimento,
                                "descrição_movimentação": descricao_movimento})
    return movimentos_list


def get_partes(response):
    partes_list = []
    partes = response.css('#tableTodasPartes .fundoClaro')
    for parte in partes:
        advogados = set([])
        nomes = parte.css('.nomeParteEAdvogado::text').getall()
        nome = clean_data(nomes[0])
        tipo_participacao = clean_data(parte.css('.tipoDeParticipacao::text').get())
        logging.info(nomes)
        for advogado in nomes[1::]:
            advogado = clean_data(advogado)
            if advogado: advogados.add(advogado)
        partes_list.append({
            "nome": nome,
            "tipoDeParticipacao": tipo_participacao,
            "advogados": list(advogados)
        })
    return partes_list


def format_data_movimentacao(movimento):
    return clean_data(movimento.css('.dataMovimentacaoProcesso::text').get())


def get_movimentos_segundo_grau(response):
    movimentos = response.css('.movimentacaoProcesso')
    movimentos_list = []
    for movimento in movimentos:
        data_movimento = format_data_movimentacao(movimento)
        descricao_movimento = format_descricao_movimentacao(movimento)

        movimentos_list.append({"data_movimentação": data_movimento,
                                "descrição_movimentação": descricao_movimento})
    return movimentos_list


def format_descricao_movimentacao(movimento):
    results_descricao_movimento = str(movimento.css('.descricaoMovimentacaoProcesso span::text').get()) + \
                                  str(movimento.css('.descricaoMovimentacaoProcesso::text').get()) + \
                                  str(movimento.css('.descricaoMovimentacaoProcesso .linkMovVincProc::text').get())

    return clean_data(results_descricao_movimento)


def clean_data(data: str):
    if data is None:
        return data
    data = data.replace("\n", "") \
        .replace("\t", "").replace("\r", "").replace("\"", '"').replace("\xa0", "").replace("None",
                                                                                            "").rstrip().lstrip()
    return re.sub(' +', ' ', data)
