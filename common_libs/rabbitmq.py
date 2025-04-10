import typing
import aio_pika
import asyncio
from aio_pika.robust_connection import AbstractRobustConnection
from aio_pika.robust_channel import AbstractRobustChannel
from aio_pika.robust_queue import AbstractRobustQueue


class RabbitMQManger:
    """
    Manages the connection to RabbitMQ and allows the creation of channels and queues.
    This class follows the Singleton design pattern to ensure that only one instance exists.
    """

    instance: typing.Optional['RabbitMQManger'] = None
    queues: typing.Dict[str, AbstractRobustQueue] = {}

    def __new__(cls, *args, **kwargs) -> 'RabbitMQManger':
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

    async def _connect(self) -> None:
        """
        Connects to RabbitMQ using the provided credentials and connection parameters.
        Retries the connection up to `max_retry_connection` times in case of failure.

        Raises:
            RuntimeError: If the maximum number of connection retries is exceeded.
        """
        retries = 0
        while retries <= self.max_retry_connection:
            try:
                self.connection = await aio_pika.connect_robust(
                    login=self.username,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    virtual_host="/",
                )
                print("Connected successfully.")
                return
            except aio_pika.exceptions.AMQPError as e:
                retries += 1
                wait_time = retries * 2
                print(f"Connection error. Waiting for {wait_time} seconds.\n{e}")
                await asyncio.sleep(wait_time)

        raise RuntimeError("Connection error: Exceeded maximum number of connection retries.")

    async def _close(self) -> None:
        """
        Closes the current connection if it is open.
        """
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            self.connection = None

    async def __aenter__(self) -> 'RabbitMQManger':
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

    async def declare_queue(self, queue_name: str) -> AbstractRobustQueue:
        """
        Declares a queue in RabbitMQ if not already declared, otherwise returns the existing queue.

        Args:
            queue_name (str): The name of the queue to declare.

        Returns:
            AbstractRobustQueue: The declared or existing queue.
        """
        if queue_name in self.queues:
            print(f"Queue '{queue_name}' already declared, returning existing one.")
            return self.queues[queue_name]

        # Declare a new queue
        channel = await self.get_channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        self.queues[queue_name] = queue  # Store the declared queue
        print(f"Queue '{queue_name}' declared successfully.")
        return queue




# async def main():
#     async with RabbitMQManger() as manager:
#         channel = await manager.get_channel()
#         queue_name= "test_ali"
#         queue = await manager.declare_queue(queue_name)
#
#         message_body = "test hello world"
#         message = aio_pika.Message(body=message_body.encode())
#         await channel.default_exchange.publish(
#             message, routing_key=queue.name
#         )
#         print(f"Message '{message_body}' sent to queue '{queue_name}'")
#
#
#
#
# if __name__ == "__main__":
#     asyncio.run(main())