"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

from passlib.context import CryptContext

from core.config import get_config
from common_libs.rabbitmq import RabbitMQManger

Setting = get_config()


hashManager = CryptContext(schemes=["bcrypt"], deprecated="auto")
rabbitManager = RabbitMQManger(
    username=Setting.RABBITMQ_USERNAME,
    password=Setting.RABBITMQ_PASSWORD,
    host=Setting.RABBITMQ_HOST,
    port=Setting.RABBITMQ_PORT,
    virtual_host=Setting.RABBITMQ_VHOST,
)
