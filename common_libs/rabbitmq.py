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
import typing
import aiologger
import aio_pika
from aio_pika.robust_channel import AbstractRobustChannel
from aio_pika.robust_connection import AbstractRobustConnection
from aio_pika.robust_queue import AbstractRobustQueue
from common_libs.logger import get_async_logger


class RabbitMQManger:
    """
    Manages the connection to RabbitMQ and allows the creation of channels and queues.
    This class follows the Singleton design pattern to ensure that only one instance exists.
    """

    instance: typing.Optional["RabbitMQManger"] = None
    queues: typing.Dict[str, AbstractRobustQueue] = {}

    def __new__(cls, *args, **kwargs) -> "RabbitMQManger":
        """
        Singleton pattern to ensure only one instance of RabbitMQManger is created.

        Returns:
            RabbitMQManger: The singleton instance.
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
        max_retry_connection: int = 10,
        virtual_host: str = "/",
    ) -> None:
        """
        Initializes the RabbitMQManger instance.

        Args:
            host (str): The RabbitMQ server hostname (default: "localhost").
            port (int): The RabbitMQ server port (default: 5672).
            username (str): RabbitMQ username (default: "guest").
            password (str): RabbitMQ password (default: "guest").
            max_retry_connection (int): The maximum number of retry attempts for connecting to RabbitMQ (default: 10).
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection: typing.Optional[AbstractRobustConnection] = None
        self.channel: typing.Optional[AbstractRobustChannel] = None
        self.max_retry_connection = max_retry_connection
        self.queues: typing.Dict[str, AbstractRobustQueue] = {}
        self.virtual_host = virtual_host

    async def setup_logger(self):
        self.logger = await get_async_logger(
            log_level=logging.INFO,
            log_file="rabbitmq.log",
            logger_name="rabbitmq-logger",
        )
        await self.logger.info("Logger Created successfully.")

    async def _connect(self) -> None:
        """
        Connects to RabbitMQ using the provided credentials and connection parameters.
        Retries the connection up to `max_retry_connection` times in case of failure.

        Raises:
            RuntimeError: If the maximum number of connection retries is exceeded.
        """
        self.logger.info(f"rabbitmq: trying to connect to {self.host}:{self.port}")
        retries = 0
        while retries <= self.max_retry_connection:
            try:
                self.connection = await aio_pika.connect_robust(
                    login=self.username,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    virtual_host=self.virtual_host,
                )
                self.logger.info(
                    f"rabbitmq: connected successfully to {self.host}:{self.port}"
                )
                return
            except aio_pika.exceptions.AMQPError as e:
                retries += 1
                wait_time = retries * 2
                self.logger.info(
                    f"rabbitmq: connection failed for {self.host}:{self.port}, retry number:{retries}, wait_for: {wait_time}s,\nreason: {e.reason}"
                )
                await asyncio.sleep(wait_time)

        self.logger.info(
            f"rabbitmq: connection failed for {self.host}:{self.port}, Connection error: Exceeded maximum number of connection retries"
        )

        raise RuntimeError(
            "Connection error: Exceeded maximum number of connection retries."
        )

    async def _close(self) -> None:
        """
        Closes the current connection if it is open.
        """
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            await self.logger.info(
                f"rabbitmq: connection to {self.host}:{self.port} closed."
            )
            self.connection = None

    async def __aenter__(self) -> "RabbitMQManger":
        """
        Asynchronous context manager entry method. Ensures the connection is established.

        Returns:
            RabbitMQManger: The current instance of the manager.
        """
        if self.connection and not self.connection.is_closed:
            return self
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Asynchronous context manager exit method. Closes the connection when exiting the context.

        Args:
            exc_type: The exception type (if any).
            exc_val: The exception value (if any).
            exc_tb: The traceback (if any).
        """
        await self._close()

    async def get_channel(self) -> AbstractRobustChannel:
        """
        Returns an active RabbitMQ channel. If no active channel exists, creates one.

        Returns:
            AbstractRobustChannel: The active RabbitMQ channel.
        """
        if self.connection is None or self.connection.is_closed:
            await self._connect()

        if self.channel is None or self.channel.is_closed:
            self.channel = await self.connection.channel()

        return self.channel

    async def declare_queue(
        self, queue_name: str, *args, **kwargs
    ) -> AbstractRobustQueue:
        """
        Declares a queue in RabbitMQ if not already declared, otherwise returns the existing queue.

        Args:
            queue_name (str): The name of the queue to declare.

        Returns:
            AbstractRobustQueue: The declared or existing queue.
        """
        if queue_name in self.queues:
            await self.logger.info(
                f"rabbitmq: Queue '{queue_name}' already declared, returning existing one."
            )
            return self.queues[queue_name]

        # Declare a new queue
        channel = await self.get_channel()
        queue = await channel.declare_queue(queue_name, *args, **kwargs)
        self.queues[queue_name] = queue  # Store the declared queue
        await self.logger.info(f"rabbitmq: Queue '{queue_name}' declared successfully.")
        return queue
