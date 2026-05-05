# jus-crawler

API que busca dados de um processo em todos os graus dos Tribunais de Justiça de São Paulo (TJSP), Alagoas (TJAL) e do Ceará (TJCE).

A api recebe o número do processo, que deve seguir
o [padrão do Conselho Nacional de Justiça para numeração de processos jurídicos](https://www.cnj.jus.br/programas-e-acoes/numeracao-unica/).

Quando o processamento termina, o usuário é capaz de coletar os dados em formato JSON.

Endereços utilizados para as consultas de processos:

* TJAL
    * 1º grau - https://www2.tjal.jus.br/cpopg/open.do
    * 2º grau - https://www2.tjal.jus.br/cposg5/open.do
* TJCE
    * 1º grau - https://esaj.tjce.jus.br/cpopg/open.do
    * 2º grau - https://esaj.tjce.jus.br/cposg5/open.do
 * TJSP
   * 1º grau - https://esaj.tjsp.jus.br/cpopg/open.do
   * 2º grau - https://esaj.tjsp.jus.br/cposg5/open.do

Dados coletados:

* classe
* área
* assunto
* data de distribuição
* juiz
* valor da ação
* partes do processo
* lista das movimentações

---
Exemplos de números de processos podem ser encontrados nos diários oficiais

* Diário oficial de Alagoas: [jusbrasil.com.br/diarios/DJAL/](https://www.jusbrasil.com.br/diarios/DJAL/)
* Diário de justiça do estado do Ceará: [jusbrasil.com.br/diarios/DJCE/](https://www.jusbrasil.com.br/diarios/DJCE/)
* Diário de justiça do estado de São Paulo: [jusbrasil.com.br/diarios/DJSP/](https://www.jusbrasil.com.br/diarios/DJSP/)

# Acesso à aplicação

Atualmente o deploy é realizado no **Google Cloud Run**.

Após o deploy, o endereço público da aplicação pode ser obtido com:

```bash
gcloud run services describe jus-crawler --region southamerica-east1 --format='value(status.url)'
```

Com a URL retornada, os acessos principais são:

* Aplicação: `https://<URL_DO_SERVICO>`
* Documentação Swagger: `https://<URL_DO_SERVICO>/docs`

## Como efetuar o deploy (Google Cloud Run)

Pré-requisitos:

* Projeto criado no Google Cloud
* APIs habilitadas:
    * Cloud Run Admin API
    * Artifact Registry API
    * Cloud Build API
* Código-fonte disponível no diretório do projeto

Passo a passo:

```bash
gcloud auth login
gcloud config set project SEU_PROJECT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
gcloud run deploy jus-crawler --source . --region southamerica-east1 --allow-unauthenticated --port 8080 --timeout 300 --memory 512Mi --min-instances 0 --max-instances 1
```

Observações:

* Não é necessário criar credenciais manualmente para esse fluxo inicial de deploy.
* Se o `gcloud` não estiver instalado localmente, use o **Cloud Shell** no console do Google Cloud.
# Organização do código

| №   | Path                                | Description                                                                                                          |
|-----|-------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| 1.  | source/                             | Diretório com toda a lógica do projeto                                                                               |
| 2.  | source/controller                   | Métodos/endpoints da API                                                                                             |
| 3.  | source/models                       | Classes com informações necessárias para processar as requisições da API                                             |
| 4.  | source/services/collect.py          | Implementação do crawler com métodos de busca e parsing dos dados                                                    |
| 5.  | source/services/parse.py            | Métodos utilizados pelo crawler para parsing dos dados                                                               |
| 6.  | source/services/tribunais_mapper.py | Estruturas que concentram todas as informações necessárias dos tribunais suportados (nome, número e domínio do site) |
| 7.  | source/services/validate.py         | Schemas contendo as regras para validação dos dados de input com [Cerberus](https://docs.python-cerberus.org)        |
| 8.  | front-end/                          | Diretório contendo arquivos estáticos e templates HTML                                                               |
| 9.  | README.md                           | Arquivo atual com a documentação do projeto                                                                          |
| 10. | tests/                              | Testes automatizados com pytest para parsing, validação e orquestração do fluxo                                      |
| 11. | requirements.txt                    | Lista dos pacotes utilizados no projeto                                                                              |

# Performance

Na branch ```async-tjal``` encontra-se o código com implementação de processamento assíncrono. Essa funcionalidade
reduziu o tempo de resposta da API, possibilitando a busca e retorno dos dados em menos de 2 segundos (em média).

Porém, uma limitação foi encontrada para estabelecer conexão com o site do TJCE utilizando essa
funcionalidade. A mensagem de erro pode ser visualizada abaixo:

```
aiohttp.client_exceptions.ClientConnectorSSLError: Cannot connect to host esaj.tjce.jus.br:443 ssl:default [TLS/SSL connection has been closed (EOF)]
```

Portanto, atualmente é possível utilizar o processamento assíncrono apenas para buscar informações de processos do TJAL.

# How to run locally

### Using [pyenv](https://github.com/pyenv/pyenv-installer)

**Ambiente local:**
```bash
pyenv install 3.11.3
pyenv virtualenv 3.11.3 env-jus_crawler
pyenv activate env-jus_crawler
pyenv local env-jus_crawler # opcional
pip install --upgrade pip
pip install -r requirements.txt
```

> **Nota:** A versão recomendada localmente é Python 3.11.3. Em produção (Cloud Run), o runtime está definido no `Dockerfile`.

## Start the service:

```bash
uvicorn source.main:app --reload
```

App will be available in http://127.0.0.1:8000

Swagger API's documentation will be available in http://127.0.0.1:8000/docs

## Automated tests

The project includes automated tests based on `pytest`, covering:
- Parsing helpers
- Input validation 
- Orchestration layer that consolidates search results
- **Front-end template rendering with multiple scenarios**

To run all tests locally:

```bash
pytest -q
```

### Front-end specific tests

20 automated tests validate template rendering with mocked process data:

```bash
# Run frontend template tests
pytest tests/test_frontend_templates.py -v

# Run specific test category
pytest tests/test_frontend_templates.py::TestHomePageRoute -v

# Run with coverage report
pytest tests/test_frontend_templates.py --cov=source.main
```

**Test scenarios covered:**
- ✅ Home and About pages render correctly
- ✅ Valid process data (1º and 2º grau) display properly
- ✅ Error handling (timeout, invalid CNJ, missing data)
- ✅ Data normalization before template rendering
- ✅ HTML structure and accessibility
- ✅ Assistant AI panel and floating button

**Status:** 15/20 tests passing (75%)

For detailed testing documentation, see [FRONTEND_TESTING.md](docs/FRONTEND_TESTING.md)

---

All tests use local HTML fixtures under `tests/` and do not depend on live requests to the tribunal portals.

---
**SQLite notes**

- This project stores subscriptions in a local SQLite database file at `data/subscriptions.db` when running with the SQLite backend.
- On Linux (Ubuntu/Debian) you must have the SQLite development headers installed before building Python so that the `_sqlite3` module is available to Python. Install system deps:

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libncurses5-dev libffi-dev liblzma-dev tk-dev libsqlite3-dev pkg-config
```

- After installing system packages, (re)install Python via `pyenv` and recreate the virtualenv (example from project):

```bash
pyenv uninstall -f 3.11.3 || true
pyenv install 3.11.3
pyenv virtualenv 3.11.3 env-jus_crawler
pyenv activate env-jus_crawler
pip install --upgrade pip
pip install -r requirements.txt
```

- Verify sqlite support in Python:

```bash
python -c "import sqlite3; print('sqlite version:', sqlite3.sqlite_version)"
```

- If you don't want to recompile Python, the project falls back to a JSON-based storage file `data/subscriptions.json` (legacy). The app will migrate JSON data to the SQLite DB automatically when SQLite is available.

**Docker notes**

- The project's Dockerfile has been adjusted to install system packages required for building and running with SQLite. If you build the image locally you will get the proper SQLite runtime support.

