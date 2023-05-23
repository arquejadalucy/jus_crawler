import re

from app.models import Parte, ParteComAdvogados


def parse_data(html):
    date = html.find(id="dataHoraDistribuicaoProcesso")
    juiz = html.find(id="juizProcesso")
    valor = html.find(id='valorAcaoProcesso')
    classe = html.find(id='classeProcesso')
    area = html.find(id="areaProcesso")
    assunto = html.find(id='assuntoProcesso')
    return {
        'classe': classe.text.lstrip().rstrip() if classe else "",
        'area': area.text.lstrip().rstrip() if area else "",
        'assunto': assunto.text if assunto else "",
        'data': date.text[0:10] if date else "",
        'juiz': juiz.text if juiz else "",
        'valor': clean_data(valor.text) if valor else "",
        'partes': get_partes(html)
    }


def parse_data_primeiro_grau(html):
    data1 = parse_data(html)
    data1.update({'movimentações': get_movimentos_primeiro_grau(html)})
    return data1


def parse_data_segundo_grau(html):
    data2 = parse_data(html)
    data2.update({'movimentações': get_movimentos_segundo_grau(html)})
    return data2


def get_movimentos_primeiro_grau(html):
    movimentos_list = []
    movimentos = html.select(".containerMovimentacao")
    for movimento in movimentos:
        data_movimento = clean_data(movimento.find(class_='dataMovimentacao').text)

        descricao_movimento = clean_data(movimento.find(class_='descricaoMovimentacao').text)

        movimentos_list.append({"data_movimentação": data_movimento,
                                "descrição_movimentação": descricao_movimento})
    return movimentos_list


def get_movimentos_segundo_grau(html):
    movimentos = html.select('.movimentacaoProcesso')
    movimentos_list = []
    for movimento in movimentos:
        data_movimento = clean_data(movimento.find(class_='dataMovimentacaoProcesso').text)
        descricao_movimento = clean_data(movimento.find(class_='descricaoMovimentacaoProcesso').text)

        movimentos_list.append({"data_movimentação": data_movimento,
                                "descrição_movimentação": descricao_movimento})
    return movimentos_list


def get_partes(html):
    partes_list = []
    partes = html.select('#tableTodasPartes tr')
    if not partes:
        partes = html.select('#tablePartesPrincipais tr')
    for item in partes:
        nomes_result = item.find(class_='nomeParteEAdvogado')
        tipo_participacao_result = item.find(class_='tipoDeParticipacao')
        nomes = clean_data(nomes_result.get_text()) if nomes_result else ""
        tipo_participacao = clean_data(tipo_participacao_result.text) if tipo_participacao_result else ""
        parte_obj = get_parte_obj(nomes, tipo_participacao)
        partes_list.append(parte_obj.dict())
    return partes_list


def get_parte_obj(nomes, tipo_de_participacao: str):
    partes = re.split(" Advogado: | Advogada: ", nomes)
    nome = partes[0]
    advogados = partes[1::]
    if advogados:
        return ParteComAdvogados(nome=nome, tipo_de_participacao=tipo_de_participacao, advogados=advogados)
    return Parte(nome=nome, tipo_de_participacao=tipo_de_participacao)


def clean_data(data: str):
    if data is None:
        return data
    data = data.replace("\n", " ").replace("&nbsp", " ").replace("&nbsp;", " ") \
        .replace("\t", " ").replace("\r", "").replace('\"', '"') \
        .replace("\xa0", "").replace("None", "").rstrip().lstrip()
    return re.sub(' +', ' ', data)
