# jus_crawler
API que busca dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE).

A api recebe o número do processo. Para descobrir o tribunal é utilizado o [padrão do Conselho Nacional de Justiça para numeração de processos jurídicos](https://www.cnj.jus.br/programas-e-acoes/numeracao-unica/).

Quando o processamento termina, o usuário é capaz de coletar os dados em formato JSON.

Endereços utilizados para as consultas de processos:
* TJAL
  * 1º grau - https://www2.tjal.jus.br/cpopg/open.do
  * 2º grau - https://www2.tjal.jus.br/cposg5/open.do
* TJCE
  * 1º grau - https://esaj.tjce.jus.br/cpopg/open.do
  * 2º grau - https://esaj.tjce.jus.br/cposg5/open.do

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
* Diário oficial de Alagoas: https://www.jusbrasil.com.br/diarios/DJAL/
* Diário de justiça do estado do Ceará: https://www.jusbrasil.com.br/diarios/DJCE/

# Organização do código
| №   | Path             | Description                                                                                                   |
|-----|------------------|---------------------------------------------------------------------------------------------------------------|
| 1.  | app/             | Diretório com toda a lógica do projeto                                                                        |
| 2.  | app/api.py       | Métodos/endpoints da API                                                                                      |
| 3.  | app/crawler.py   | Implementação do crawler com métodos de busca e parsing dos dados                                             |
| 4.  | app/enums.py     | Estruturas que concentram informações necessárias dos tribunais suportados (nome, número e domínio do site)   |
| 5.  | app/models.py    | Classes para informações necessárias para processar as requisições da API                                     |
| 5.  | app/schemas.py   | Schemas contendo as regras para validação dos dados de input com [Cerberus](https://docs.python-cerberus.org) |
| 6.  | app/utils.py     | Métodos utilizados pelo crawler para parsing dos dados                                                        |
| 7.  | tests/           | Diretório com os testes do projeto                                                                            |
| 8.  | tests/Stubs.py   | Arquivo com dados utilizados nos testes                                                                       |
| 9.  | tests/Tests.py   | Classes de testes automatizados                                                                               |
| 10. | README.md        | Arquivo atual com a documentação do projeto                                                                   |
| 11. | requirements.txt | Lista dos pacotes utilizados no projeto                                                                       |

# How to run

## Install the requirements:
```bash
pip install -r requirements.txt
```
## Start the service:
```bash
uvicorn app.api:app --reload
```
Service will be available in http://127.0.0.1:8000

API's documentation will be available in http://127.0.0.1:8000/docs
# Tests
## Run tests with coverage
```bash
coverage run -m pytest tests\Tests.py
```
## See coverage report
```bash
coverage report
```
## Generate coverage report html
```bash
coverage html
```
Html coverage report page will be available in [htmlcov/index.html](http://localhost:63342/jus_crawler/htmlcov/index.html)
