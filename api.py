import logging
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info('FastAPI сервер запущен')

@app.get('/')
def read_root():
    logger.info('Запрос к корневому эндпоинту')
    return {'Hello': 'World'}
