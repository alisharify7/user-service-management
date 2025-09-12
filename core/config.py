"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

import pathlib
from pathlib import Path

import redis.asyncio as redis
from decouple import config

from common_libs.utils import generate_random_string


class BaseSetting:
    """Base Setting class"""

    SECRET_KEY: str = config("APP_SECRET_KEY", generate_random_string())
    if not config("APP_SECRET_KEY", False):
        print(  # TODO: use logger instead of print
            "SECRET_KEY was not found in environment variables, fall back "
            "into generate_random_string() function. "
        )
    DEBUG: bool = config("APP_DEBUG", "") == "True"
    BASE_DIR: pathlib.Path = Path(__file__).parent.parent.resolve()

    # main API config
    API_NAME: str = config("API_NAME", "api-service")
    API_REDOC_URL: str = config("API_REDOC_URL", "/redoc")
    API_SWAGGER_URL: str = f'{config("API_SWAGGER_URL", "/swagger")}'
    API_ABSOLUTE_VERSION: str = config("API_ABSOLUTE_VERSION", "1.0.0")
    API_SHORT_VERSION: str = config("API_SHORT_VERSION", "1.0.0")
    API_SUMMERY: str = config("API_SUMMERY", "")
    API_DESCRIPTION: str = config("API_DESCRIPTION", "")
    API_TERM_URL: str = config("API_TERM", "/term")
    API_BASE_URL: str = f"/{config('API_BASE_URL', 'api')}/v{API_SHORT_VERSION}/"

    # database config
    DATABASE_NAME: str = config("DATABASE_NAME")
    DATABASE_PORT: str = config("DATABASE_PORT")
    DATABASE_HOST: str = config("DATABASE_HOST")
    DATABASE_USERNAME: str = config("DATABASE_USERNAME")
    DATABASE_PASSWORD: str = config("DATABASE_PASSWORD")
    DATABASE_TABLE_PREFIX_NAME: str = config("DATABASE_TABLE_PREFIX")
    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql+asyncpg://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG_QUERY: bool = config("DATABASE_DEBUG_QUERY", False)  # sqlalchemy echo config

    def __str__(self):
        return "BaseSetting Class"

    def __repr__(self):
        return self.__str__()


class Setting(BaseSetting):
    """universal config class
    every property on this class will be automatically mapping to app.config
    """

    # redis config
    REDIS_DEFAULT_URI: str = config("REDIS_DEFAULT_URI", "localhost")
    REDIS_DEFAULT_INTERFACE = redis.Redis().from_url(REDIS_DEFAULT_URI)

    REDIS_CACHE_URI = config("REDIS_CACHE_URI", "localhost")
    REDIS_CACHE_INTERFACE = redis.Redis().from_url(REDIS_CACHE_URI)

    REDIS_API_KEY_URI: str = config("REDIS_API_KEY_URI", "localhost")
    REDIS_API_KEY_INTERFACE = redis.Redis.from_url(REDIS_API_KEY_URI)

    #  s3 object storage config
    AWS_BUCKET_NAME: str = config("AWS_BUCKET_NAME", "")
    AWS_ACCESS_KEY_ID: str = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = config("AWS_SECRET_ACCESS_KEY")
    AWS_ENDPOINT_URL: str = config("AWS_WRITE_ENDPOINT_URL")
    AWS_READ_ENDPOINT_URL: str = config("AWS_READ_ENDPOINT_URL")

    # RabbitMQ Config
    RABBITMQ_USERNAME: str = config("RABBITMQ_USERNAME")
    RABBITMQ_PASSWORD: str = config("RABBITMQ_PASSWORD")
    RABBITMQ_HOST: str = config("RABBITMQ_HOST")
    RABBITMQ_PORT: int = (
        5672
        if not config("RABBITMQ_PORT").isnumeric()
        else int(config("RABBITMQ_PORT"))
    )
    RABBITMQ_VHOST: str = config("RABBITMQ_VHOST")

    def __str__(self):
        return "Setting Class"

    def __repr__(self):
        return self.__str__()


class Production(Setting):
    """Production config class

    use this class for Production config class.
    """

    DEBUG: bool = False

    def __str__(self):
        return "Production Config Class"

    def __repr__(self):
        return self.__str__()


class Development(Setting):
    """Development config class

    use this class for Development config class.
    """

    DEBUG: bool = True

    def __str__(self):
        return "Development Config Class"

    def __repr__(self):
        return self.__str__()


def get_config(debug: bool = BaseSetting.DEBUG) -> object:
    """Getting config setting class base on `environment` status.
    :return: object
    :rtype: object
    """
    match debug:
        case True:
            return Development
        case False:
            return Production
        case _:
            return Production
