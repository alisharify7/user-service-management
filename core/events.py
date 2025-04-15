"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core import extensions


@asynccontextmanager
async def lifespan(app: FastAPI):
    from users.rabbit_operation import consume_users_messages

    await extensions.rabbitManager.setup_logger()
    # rabbit_task = asyncio.create_task(consume_users_messages())

    yield
    await extensions.rabbitManager.logger.shutdown()
