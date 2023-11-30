import re

from source.models.Movimentacao import Movimentacao
from source.models.Parte import Parte


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
    data1.update({'movimentações': get_movimentos(grau=1, html=html)})
    return data1


def parse_data_segundo_grau(html):
    data2 = parse_data(html)
    data2.update({'movimentações': get_movimentos(grau=2, html=html)})
    return data2


def get_movimentos(grau, html):
    tags_por_grau = {
        1: {
            "container": ".containerMovimentacao",
            "data": 'dataMovimentacao',
            "descricao": "descricaoMovimentacao"
        },
        2: {
            "container": ".movimentacaoProcesso",
            "data": 'dataMovimentacaoProcesso',
            "descricao": "descricaoMovimentacaoProcesso"
        }
    }
    movimentos_list = []
    tags = tags_por_grau.get(grau)
    movimentos = html.select(tags.get("container"))
    for movimento in movimentos:
        data_movimento = clean_data(
            movimento.find(class_=tags.get("data")).text)

        descricao_movimento = clean_data(
            movimento.find(class_=tags.get("descricao")).text)

        movimentos_list.append(
            Movimentacao(data=data_movimento,
                         descricao=" ".join(descricao_movimento.split()))
        )
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
        partes_list.append(parte_obj.__dict__)
    return partes_list


def get_parte_obj(nomes, tipo_de_participacao: str):
    partes = re.split(" Advogado: | Advogada: ", nomes)
    nome = clean_data(partes[0])
    advogados = [clean_data(adv) for adv in partes[1::]]
    return Parte(nome, tipo_de_participacao, advogados)


def clean_data(data: str):
    if data is not None:
        data = data.replace("\n", " ").replace("&nbsp", " ").replace("&nbsp;", " ") \
            .replace("\t", " ").replace("\r", "").replace('\"', '"') \
            .replace("\xa0", "").replace("None", "").strip()
        re.sub(' +', ' ', data)
    return data
