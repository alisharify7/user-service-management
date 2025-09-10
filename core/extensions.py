"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

from passlib.context import CryptContext

from common_libs.rabbitmq import RabbitMQManger
from core.config import get_config

Setting = get_config()


hashManager: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
rabbitManager: RabbitMQManger = RabbitMQManger(
    username=Setting.RABBITMQ_USERNAME,
    password=Setting.RABBITMQ_PASSWORD,
    host=Setting.RABBITMQ_HOST,
    port=Setting.RABBITMQ_PORT,
    virtual_host=Setting.RABBITMQ_VHOST,
)
