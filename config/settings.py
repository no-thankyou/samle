import os

from pydantic import HttpUrl, MySQLDsn, RedisDsn
from pydantic_settings import BaseSettings

TEST = True if os.getenv('TEST') else False
DEBUG = True if os.getenv('DEBUG') else False
BASE_DIR = os.path.dirname(__file__)


class Settings(BaseSettings):
    DEBUG: bool = True
    PROJECT_NAME: str = 'Backend Crypto Async'
    SERVICE_URL: HttpUrl = 'http://localhost:8000'
    VERSION: str = '0.0.1'

    MYSQL_ASYNC_URL: MySQLDsn = 'mysql+aiomysql://root:root@localhost:3306/mt'
    REDIS_URL: RedisDsn = 'redis://localhost:6379'

    ENVIRONMENT_NAME: str = 'local'
    ELASTIC_APM_URL: str = ''

    SENTRY_DSN: str = ''

    class Config:
        env_file = 'config/.env' if not TEST else 'config/.env.test'
        env_file_encoding = "utf-8"


settings = Settings()

__all__ = ["settings"]
