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

    await extensions.rabbit_manager.setup_logger(
        logger_name="rabbitmq-consumer", log_file="rabbitmq-consumer.log"
    )
    asyncio.create_task(consume_users_messages())

    # for i in range(10):
    #     d = UserEvent(event_type=UserEventType.UPDATED,
    #                   data=CreateUserEvent(username=f"from_rabbitmq{f"{random.randint(1,64)}" if i in [2,6,4] else ""}", password="pass",
    #                                        gender=Gender.male, phone_number=f"rabbit{f"{random.randint(1,64)}" if i in [2,6,4] else ""}",
    #                                        email_address=f"rabbit{f"{random.randint(1,64)}" if i in [2,6,4] else ""}@mq.ir"))
    #
    #     async with extensions.rabbitManager as rabbit_manager:
    #         channel = await rabbit_manager.get_channel()
    #         await channel.default_exchange.publish(
    #             aio_pika.Message(
    #                 body=(d.model_dump_json()).encode(),
    #                 delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
    #             ),
    #             routing_key="users_queue",
    #         )
    #         await rabbit_manager.logger.info("Message published.")

    yield
    await extensions.rabbit_manager.logger.shutdown()
