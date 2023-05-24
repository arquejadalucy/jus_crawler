# crawler_jus
API que busca dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE).

# Como executar
```bash
# Install the requirements:
pip install -r requirements.txt
# Start the service:
uvicorn api:app --reload
# Tests
## Run tests with coverage
coverage run ApiTests.py
## See coverqage report
coverage report
coverage html

```