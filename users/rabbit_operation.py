"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

import json

from aio_pika import Message, IncomingMessage
from users.scheme import UserEvent
from users.operations import create_user, delete_user, update_user
from core.db import get_session
from core.extensions import rabbitManager, logger


async def consume_users_messages():
    queue = await rabbitManager.declare_queue("users_queue", durable=True)
    async with queue.iterator(no_ack=False) as queue_iter:
        async for message in queue_iter:
            try:
                await logger.info("Message consumed successfully.")
                user_data = UserEvent.model_validate_strings(message.body.decode())
            except json.JSONDecodeError:
                message.nack(requeue=False)
                await logger.info("error in validating consumed message.")
                return

            if user_data.event_type.CREATED:
                await process_create_users(user_data)
            elif user_data.event_type.UPDATED:
                await process_update_users(user_data)
            else:
                await process_delete_users(user_data)
            await logger.info(f"Received message: {message.body.decode()}")


async def process_create_users(message: IncomingMessage, user_data: UserEvent):
    async with get_session() as session:
        result = await create_user(db_session=session, user_data=user_data.model_dump())
        if len(result) != 1:
            await logger.info(f"db error in creating user. {user_data.model_dump()}")
            await message.nack(requeue=True)

        await logger.info(f"user created successfully. {user_data.model_dump()}")
        await message.ack()


async def process_delete_users(message: IncomingMessage, user_data: UserEvent):
    async with get_session() as session:
        result = await delete_user(db_session=session, user_id=user_data.data.id)
        if len(result) != 1:
            await logger.info(f"db error in deleting user. {user_data.model_dump()}")
            await message.nack(requeue=True)

        await logger.info(f"user deleted successfully. {user_data.model_dump()}")
        await message.ack()


async def process_update_users(message: IncomingMessage, user_data):
    async with get_session() as session:
        result = await update_user(
            db_session=session,
            user_id=user_data.data.id,
            user_data=user_data.model_dump(),
        )
        if len(result) != 1:
            await logger.info(f"db error in updating user. {user_data.model_dump()}")
            await message.nack(requeue=True)

        await logger.info(f"user updated successfully. {user_data.model_dump()}")
        await message.ack()
