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

| №   | Path                                | Descrição                                                                                                            |
|-----|-------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| 1.  | source/                             | Diretório com toda a lógica do projeto                                                                               |
| 2.  | source/main.py                      | Entrypoint FastAPI; define endpoints públicos (/buscaprocesso, /subscribe, /unsubscribe) e admin (/admin/scheduler, /admin/check) |
| 3.  | source/controller/                  | Camada de controllers com rotas da API                                                                              |
| 4.  | source/controller/processos.py      | Endpoints de busca de processos com instrumentação de tempo de execução                                             |
| 5.  | source/models/                      | Classes de dados (NumeroProcessoInfo, ProcessoRequestBody, etc.)                                                     |
| 6.  | source/services/collect.py          | Crawler com métodos de busca e parsing dos dados; inferência de tribunal no payload                                 |
| 7.  | source/services/parse.py            | Métodos de parsing dos dados HTML dos tribunais                                                                      |
| 8.  | source/services/tribunais_mapper.py | Mapeamento de tribunais suportados (nome, sigla, domínio)                                                           |
| 9.  | source/services/validate.py         | Schemas de validação de input com [Cerberus](https://docs.python-cerberus.org)                                      |
| 10. | source/services/subscriptions.py     | Gerenciamento de inscrições em SQLite (com migração de JSON legado)                                                  |
| 11. | source/services/notifications.py     | Envio de emails (confirmação e atualização); suporta SMTP ou demo logging em /tmp/juscrawler_notifications.log      |
| 12. | source/services/scheduler.py         | Agendador em background para verificação automática de movimentações e notificação                                   |
| 13. | front-end/                          | Diretório com arquivos estáticos e templates HTML                                                                    |
| 14. | front-end/templates/                | Templates Jinja2 (home.html, processo.html, sobre.html, unsubscribe.html)                                          |
| 15. | front-end/static/                   | Arquivos CSS (style.css, style-process.css, style-about.css)                                                        |
| 16. | tests/                              | Testes automatizados com pytest para parsing, validação e orquestração                                               |
| 17. | requirements.txt                    | Dependências do projeto                                                                                              |
| 18. | README.md                           | Documentação do projeto (este arquivo)                                                                               |

# Funcionalidades de Notificação e Acompanhamento

## Inscrição e Acompanhamento de Processos

Os usuários podem se inscrever para receber notificações automáticas sobre novos eventos em um processo:

- **Endpoint de Inscrição:** `POST /subscribe`
  - Parâmetros: `id_processo`, `contato` (email)
  - Retorna: página de confirmação com mensagem de sucesso/erro

- **Endpoint de Cancelamento:** `GET /unsubscribe`
  - Parâmetros: `cnj`, `email`
  - Link automático gerado em cada email de notificação para fácil descadastro

## Sistema de Notificações

O sistema suporta duas modalidades de notificação:

1. **Demo Mode (desenvolvimento):** Logs são salvos em `/tmp/juscrawler_notifications.log`
2. **Produção (SMTP):** Emails enviados via configuração SMTP

Configuração via variáveis de ambiente (`.env`):
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_app
SENDER_EMAIL=seu_email@gmail.com
APP_BASE_URL=http://localhost:8000
```

## Agendador de Verificação Automática

Um agendador em background verifica automaticamente novos eventos em processos com inscrições ativas:

- **Intervalo padrão:** 12 horas (configurável via `CHECK_INTERVAL_SECONDS` em `.env`)
- **Comportamento:** Agrupa por CNJ, busca a última movimentação e notifica inscritos sobre mudanças

## Endpoints Administrativos

### `POST /admin/scheduler` — Configurar intervalo

Ajusta o intervalo de verificação automática em tempo de execução.

```json
{
  "interval_seconds": 3600
}
```

### `POST /admin/check` — Enviar email de demonstração

Envia um email de notificação para um endereço informado com a última movimentação armazenada de um CNJ (sem consultar o tribunal).

```json
{
  "cnj": "0000000-00.0000.0.00.0000",
  "email": "usuario@example.com"
}
```

**Resposta:**
```json
{
  "ok": true,
  "queued": false,
  "cnj": "0000000-00.0000.0.00.0000",
  "email": "usuario@example.com"
}
```

---

# Performance

Na branch ```async-tjal``` encontra-se o código com implementação de processamento assíncrono. Essa funcionalidade
reduziu o tempo de resposta da API, possibilitando a busca e retorno dos dados em menos de 2 segundos (em média).

Porém, uma limitação foi encontrada para estabelecer conexão com o site do TJCE utilizando essa
funcionalidade. A mensagem de erro pode ser visualizada abaixo:

```
aiohttp.client_exceptions.ClientConnectorSSLError: Cannot connect to host esaj.tjce.jus.br:443 ssl:default [TLS/SSL connection has been closed (EOF)]
```

Portanto, atualmente é possível utilizar o processamento assíncrono apenas para buscar informações de processos do TJAL.

# Como Executar Localmente

### Usando [pyenv](https://github.com/pyenv/pyenv-installer)

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

### Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis necessárias:

```bash
# Scheduler (em segundos; padrão 12 horas)
CHECK_INTERVAL_SECONDS=43200

# Email (demo mode se não configurado)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_app
SENDER_EMAIL=seu_email@gmail.com

# Base URL para links (ex: unsubscribe)
APP_BASE_URL=http://localhost:8000
```

Se `SMTP_USER` e `SMTP_PASSWORD` não forem definidos, o sistema falará em demo mode e registrará notificações em `/tmp/juscrawler_notifications.log`.

### Iniciar o serviço

```bash
uvicorn source.main:app --reload
```

A aplicação estará disponível em http://127.0.0.1:8000

A documentação Swagger estará disponível em http://127.0.0.1:8000/docs

 Automatizados

O projeto inclui testes automatizados com `pytest`, cobrindo:
- Parsing e extração de dados
- Validação de entrada
- Orquestração e consolidação de resultados
- **Renderização de templates com múltiplos cenários**

Para rodar todos os testes localmente:

```bash
pytest -q
```

### Testes específicos do front-end

20 testes automatizados validam a renderização de templates com dados de processos simulados:

```bash
# Rodar todos os testes do front-end
pytest tests/test_frontend_templates.py -v

# Rodar uma categoria específica de testes
pytest tests/test_frontend_templates.py::TestHomePageRoute -v

# Rodar com relatório de cobertura
pytest tests/test_frontend_templates.py --cov=source.main
```

**Cenários cobertos:**
- ✅ Página inicial e sobre renderizam corretamente
- ✅ Dados de processo válidos (1º e 2º grau) exibem corretamente
- ✅ Tratamento de erros (timeout, CNJ inválido, dados faltando)
- ✅ Normalização de dados antes de renderizar no template
- ✅ Estrutura HTML e acessibilidade
- ✅ Formulário de inscrição e cancelamento

Todos os testes usam fixtures HTML locais em `tests/` e não dependem de requisições ao vivo para os portais dos tribunais.

## Banco de dados SQLite

O projeto armazena inscrições em um banco de dados SQLite local em `data/subscriptions.db`:

- **Migração automática:** Se você tiver um arquivo JSON legado em `data/subscriptions.json`, será migrado automaticamente ao iniciar a aplicação.
- **Fallback:** Se o SQLite não estiver disponível, o projeto usa armazenamento em JSON (legado).

**Em Linux (Ubuntu/Debian):** Instale as dependências de desenvolvimento do SQLite antes de compilar Python:

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libncurses5-dev libffi-dev liblzma-dev tk-dev libsqlite3-dev pkg-config
```

Após instalar as dependências do sistema, reinstale Python via `pyenv` e recrie o virtualenv:

```bash
pyenv uninstall -f 3.11.3 || true
pyenv install 3.11.3
pyenv virtualenv 3.11.3 env-jus_crawler
pyenv activate env-jus_crawler
pip install --upgrade pip
pip install -r requirements.txt
```

Verifique o suporte a SQLite em Python:

```bash
python -c "import sqlite3; print('sqlite version:', sqlite3.sqlite_version)"
```

**Docker:** O Dockerfile foi ajustado para instalar os pacotes do sistema necessários para compilar e executar com suporte a SQLite. Se você compilar a imagem localmente, terá suporte de runtime SQLite adequado.

---
