"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""
import logging
from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from core.config import get_config
from core.urls import urlpatterns
from core.db import BaseModelClass, engine
from core.extensions import logger, rabbitManager


Settings = get_config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    from common_libs.logger import get_async_logger

    global logger
    logger = await get_async_logger(
        log_level=logging.INFO,
        logger_name="user-service",
        log_file="app.log"
    )
    app.state.logger = logger
    rabbitManager.attach_logger(logger)
    await logger.info("test")

    async with rabbitManager as manager:
        channel = await manager.get_channel()
        queue_name= "test_ali"
        queue = await manager.declare_queue(queue_name)

        message_body = "test hello world"
        message = aio_pika.Message(body=message_body.encode())
        await channel.default_exchange.publish(
            message, routing_key=queue.name
        )
        print(f"Message '{message_body}' sent to queue '{queue_name}'")



    yield
    await logger.shutdown()

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
        lifespan=lifespan
    )

    add_pagination(app)

    for router in urlpatterns:
        app.include_router(
            router["router"], prefix=router["prefix"], tags=router["tags"]
        )

    return app


app = create_app(Settings)
import core.base_views

