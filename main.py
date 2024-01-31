import uvicorn
from fastapi import FastAPI

from config.settings import settings
from config.setup import setup

app = FastAPI(title=settings.PROJECT_NAME)
setup(app)


if __name__ == "__main__":
    host, port = settings.SERVICE_URL.host, int(settings.SERVICE_URL.port)
    if settings.DEBUG:
        uvicorn.run('main:app', host=host, port=port, reload=True)
    else:
        uvicorn.run('main:app', host=host, port=port)
