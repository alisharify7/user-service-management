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

from fastapi import FastAPI

from core import extensions
from common_libs.logger import get_async_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    extensions.logger = await get_async_logger(
        log_level=logging.INFO, logger_name="user-service", log_file="app.log"
    )
    extensions.rabbitManager.attach_logger(extensions.logger)

    from users.rabbit_operation import produce_users_messages, consume_users_messages

    await produce_users_messages()
    await consume_users_messages()
    extensions.logger.info(f"Starting application, {app.__doc__}")

    yield
    await extensions.logger.shutdown()
