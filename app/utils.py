import re


def get_area_processo(response):
    return response.css('#areaProcesso span::text').get()


def parse_data(html):
    return {
        'classe': html.find(id='classeProcesso').text.lstrip().rstrip(),
        'area': html.find(id="areaProcesso").text.lstrip().rstrip(),
        'assunto': html.find(id='assuntoProcesso').text,
        'valor': clean_data(html.find(id='valorAcaoProcesso').text),
        'partes': get_partes(html)
    }


def parse_data_primeiro_grau(html):
    date = html.find("div", id="dataHoraDistribuicaoProcesso").text

    data1 = parse_data(html)
    data1.update({'data': date[0:10] if date else ""})
    data1.update({'juiz': html.find("span", id='juizProcesso').text})
    data1.update({'movimentações': get_movimentos_primeiro_grau(html)})
    return data1


def parse_data_segundo_grau(html):
    data2 = parse_data(html)
    data2.update({"valor": "R$ " + data2.get("valor")})
    data2.update({'movimentações': get_movimentos_segundo_grau(html)})
    return data2


def get_movimentos_primeiro_grau(html):
    movimentos_list = []
    movimentos = html.select(".containerMovimentacao")
    for movimento in movimentos:
        data_movimento = clean_data(movimento.find("td", class_='dataMovimentacao').text)

        descricao_movimento = clean_data(movimento.find("td", class_='descricaoMovimentacao').text)

        movimentos_list.append({"data_movimentação": data_movimento,
                                "descrição_movimentação": descricao_movimento})
    return movimentos_list


def get_movimentos_segundo_grau(html):
    movimentos = html.select('.movimentacaoProcesso')
    movimentos_list = []
    for movimento in movimentos:
        data_movimento = clean_data(movimento.find("td", class_='dataMovimentacaoProcesso').text)
        descricao_movimento = clean_data(movimento.find("td", class_='descricaoMovimentacaoProcesso').text)

        movimentos_list.append({"data_movimentação": data_movimento,
                                "descrição_movimentação": descricao_movimento})
    return movimentos_list


def get_partes(html):
    partes_list = []
    partes = html.select('#tableTodasPartes tr')
    for item in partes:
        nomes = clean_data(item.find("td", class_='nomeParteEAdvogado').get_text())
        tipo_participacao = clean_data(item.find("span", class_='tipoDeParticipacao').text)
        nomes_parte = re.split(" Advogado: | Advogada: ", nomes)
        partes_list.append({
            "nome": nomes_parte[0],
            "tipoDeParticipacao": tipo_participacao,
            "advogados": nomes_parte[1::]
        })
    return partes_list


def clean_data(data: str):
    if data is None:
        return data
    data = data.replace("\n", " ").replace("&nbsp", " ") \
        .replace("\t", "").replace("\r", "").replace("\"", '"')\
        .replace("\xa0", "").replace("None", "").rstrip().lstrip()
    return re.sub(' +', ' ', data)
