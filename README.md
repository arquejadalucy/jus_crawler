# crawler_jus
API que busca dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE).

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
