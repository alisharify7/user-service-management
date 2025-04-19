"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

import asyncio
import json

from aio_pika import IncomingMessage
from users.scheme import UserEvent
from users.operations import create_user, delete_user, update_user
from core.db import rabbit_get_session as get_session
from core.extensions import rabbitManager


async def process_consumed_message(message):
    await rabbitManager.logger.info(
        f"Message consumed successfully. message_size: {message.body_size}, message_id: {message.message_id}"
    )

    try:
        user_data = UserEvent.model_validate_json(json_data=message.body.decode())
    except json.JSONDecodeError as e:
        await message.nack(requeue=False)
        await rabbitManager.logger.info(
            f"error in validating consumed message with message_id: {message.message_id}. error {e}"
        )
        return
    if user_data.event_type.CREATED:
        await rabbitManager.logger.info(
            f"Message Type is {user_data.event_type.CREATED} for message_id: {message.message_id}"
        )
        await process_create_users(user_data=user_data, message=message)
    elif user_data.event_type.UPDATED:
        await rabbitManager.logger.info(
            f"Message Type is {user_data.event_type.UPDATED} for message_id: {message.message_id}"
        )
        await process_update_users(user_data=user_data, message=message)
    else:
        await rabbitManager.logger.info(
            f"Message Type is {user_data.event_type.DELETED} for message_id: {message.message_id}"
        )
        await process_delete_users(user_data=user_data, message=message)


async def consume_users_messages():
    queue = await rabbitManager.declare_queue(
        "users_queue", "consume_users_operation_channel", durable=True
    )
    await queue.consume(process_consumed_message)


async def process_create_users(message: IncomingMessage, user_data: UserEvent):
    async with get_session() as session:
        result = await create_user(
            db_session=session, user_data=user_data.data.model_dump()
        )
        if len(result) != 1:
            await rabbitManager.logger.info(
                f"db error in creating user. {result}, for message_id: {message.message_id}"
            )
            await message.nack(requeue=False)
            return

        await rabbitManager.logger.info(
            f"user created successfully, for message_id: {message.message_id}"
        )
        await message.ack()


async def process_delete_users(message: IncomingMessage, user_data: UserEvent):
    async with get_session() as session:
        result = await delete_user(db_session=session, user_id=user_data.data.id)
        if len(result) != 1:
            await rabbitManager.logger.info(
                f"db error in deleting user. {result}, for message_id: {message.message_id}"
            )
            await message.nack(requeue=False)
            return

        await rabbitManager.logger.info(
            f"user deleted successfully, for message_id: {message.message_id}"
        )
        await message.ack()


async def process_update_users(message: IncomingMessage, user_data):
    async with get_session() as session:
        result = await update_user(
            db_session=session,
            user_id=user_data.data.id,
            user_data=user_data.model_dump(),
        )
        if len(result) != 1:
            await rabbitManager.logger.info(
                f"db error in updating user. {result}, for message_id: {message.message_id}"
            )
            await message.nack(requeue=False)
            return
        await rabbitManager.logger.info(
            f"user updated successfully, for message_id: {message.message_id}"
        )
        await message.ack()
