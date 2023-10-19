import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor

import aiohttp
from bs4 import BeautifulSoup

from app.tribunais_mapper import Tribunais, DominiosPorTribunal
from app.models import ProcessRequestInformations
from app.utils import parse_data_primeiro_grau, parse_data_segundo_grau, clean_data

ERROR = "ERROR"
max_concurrency = 10000
sem = asyncio.Semaphore(max_concurrency)


async def busca_primeiro_grau(processo: ProcessRequestInformations, dominio: str, session):
    data = {"id": processo.numero_processo}
    url = f"https://{dominio}/cpopg/show.do?&processo.foro={processo.foro}" \
          f"&processo.numero={processo.numero_processo}"

    html = await send_request_and_get_response(url, session=session)

    if type(html) == dict and ERROR in html:
        result = html
    else:
        result = parse_data_primeiro_grau(html)

    data.update({"Primeiro Grau": result})

    return data


async def busca_codigo_segundo_grau(url: str, session):
    codigo = ""
    html = await send_request_and_get_response(url, session=session)

    if type(html) == dict and ERROR in html:
        return ""

    elif html.find(class_='modal__lista-processos'):
        codigo = html.find(id='processoSelecionado').get('value')

    return codigo


async def busca_segundo_grau(processo: ProcessRequestInformations, dominio: str, session):
    data = {"id": processo.numero_processo}
    url = f"https://{dominio}/cposg5/search.do?" \
          f"cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={processo.numeroDigitoAnoUnificado}" \
          f"&foroNumeroUnificado={processo.foro}&dePesquisaNuUnificado={processo.numero_processo}" \
          f"&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"
    codigo = await busca_codigo_segundo_grau(url, session=session)
    if codigo:
        url = f"https://{dominio}/cposg5/show.do?processo.codigo={codigo}"

    html = await send_request_and_get_response(url, session=session)

    if type(html) == dict and ERROR in html:
        result = html
    else:
        result = parse_data_segundo_grau(html)

    data.update({"Segundo Grau": result})
    return data


async def send_request_and_get_response(url, session):
    async with session.get(f"{url}") as response:
        result = BeautifulSoup(await response.text(), "lxml")

        if result.find(id='mensagemRetorno'):
            error = clean_data(result.find(id='mensagemRetorno').find("li").text)
            logging.error(error)
            result = {ERROR: error}
        return result


async def search_process_data(process: ProcessRequestInformations):
    nome_tribunal = Tribunais(process.tribunal).name
    dominio = str(DominiosPorTribunal[nome_tribunal].value)

    async with aiohttp.ClientSession() as session:
        tasks = [
            busca_primeiro_grau(process, dominio, session),
            busca_segundo_grau(process, dominio, session)
        ]
        results = await asyncio.gather(*tasks)

        return dict((key,d[key]) for d in results for key in d)


async def run():
    processo = ProcessRequestInformations('0710802-55.2018.8.02.0001')
    print(await search_process_data(processo))


if __name__ == "__main__":
    asyncio.run(run())
