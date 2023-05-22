# crawler_jus
API que busca dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE).

# Como executar
```bash
# Install the requirements:
pip install -r requirements.txt
# Go to the api path
cd crawler_jus/api
# Start the service:
uvicorn api:app --reload
```