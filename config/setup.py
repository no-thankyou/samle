import logging
from pathlib import Path

import sentry_sdk
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from app.routers.routings import api_router
from config.settings import settings

PYPROJECT_PATH = Path(__file__).parents[1].joinpath("pyproject.toml")


def setup(app: FastAPI):
    app.version = settings.VERSION
    if settings.ENVIRONMENT_NAME != 'local':
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[
                FastApiIntegration(),
                LoggingIntegration(
                    level=logging.DEBUG,  # Capture info and above as breadcrumbs
                    event_level=logging.ERROR  # Send errors as events
                )
            ],
            environment=settings.SENTRY_ENVIRONMENT,
            # before_send=before_send,  # TODO добавить функцию для обработки сообщений
            # traces_sample_rate=1.0,
        )
        app.add_middleware(SentryAsgiMiddleware)

    if settings.ELASTIC_APM_URL:
        apm = make_apm_client({'SERVICE_NAME': settings.PROJECT_NAME})
        app.add_middleware(ElasticAPM, client=apm)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
