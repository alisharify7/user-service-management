"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from core.config import get_config
from core.db import BaseModelClass, engine
from core.events import lifespan
from core.urls import urlpatterns

Settings = get_config()


def create_app(config_class: object) -> FastAPI:
    """main factory function for generation fastapi application"""
    app = FastAPI(
        debug=config_class.DEBUG,
        title=config_class.API_NAME,
        summary=config_class.API_SUMMERY,
        description=config_class.API_DESCRIPTION,
        version=config_class.API_ABSOLUTE_VERSION,
        docs_url=config_class.API_SWAGGER_URL,
        redoc_url=config_class.API_REDOC_URL,
        terms_of_service=config_class.API_TERM_URL,
        lifespan=lifespan,
    )
    add_pagination(app)

    for router in urlpatterns:
        app.include_router(
            router["router"], prefix=router["prefix"], tags=router["tags"]
        )

    return app


app = create_app(Settings)
import core.base_views
