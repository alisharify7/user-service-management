"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

from aio_pika import Message, IncomingMessage
from pika.delivery_mode import DeliveryMode

from core.extensions import rabbitManager, logger


async def consume_users_messages():
    queue = await rabbitManager.declare_queue("users_queue", durable=True)
    async with queue.iterator(no_ack=False) as queue_iter:
        async for message in queue_iter:
            try:
                await logger.info(f"Received message: {message.body.decode()}")

                await process_users_message(message)

                await message.ack()

            except Exception as e:
                await logger.info(f"Error processing message: {e}")
                await message.nack(requeue=False)


async def process_users_message(message: IncomingMessage):
    await message.ack()


async def produce_users_messages():
    channel = await rabbitManager.get_channel()
    queue = await rabbitManager.declare_queue("users_queue", durable=True)
    message_body = "Hello, RabbitMQ!"
    message = Message(
        body=message_body.encode(), delivery_mode=DeliveryMode.Persistent.value
    )
    await channel.default_exchange.publish(message, routing_key=queue.name)
