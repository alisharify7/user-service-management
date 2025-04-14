"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

import asyncio
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
    await extensions.logger.info(f"Starting application.")

    extensions.rabbitManager.attach_logger(extensions.logger)

    # from users.rabbit_operation import consume_users_messages
    # rabbit_task = asyncio.create_task(consume_users_messages())

    yield
    await extensions.logger.shutdown()
