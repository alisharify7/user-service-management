# 👥 User Management Microservice (FastAPI + RabbitMQ)


A FastAPI-based microservice for user management with RabbitMQ event integration, providing RESTful APIs and message queue support for distributed systems.

## fully async support  async DB orm (sqlalchemy), async logging (stdout, file + rotation), async redis, async rabbitmq 

## Tech Stack
<div>
	<img src="https://skillicons.dev/icons?i=python"/>
	<img src="https://skillicons.dev/icons?i=fastapi"/>
	<img src="https://skillicons.dev/icons?i=postgresql"/>
    <img src="https://skillicons.dev/icons?i=rabbitmq"/>
    <img src="https://skillicons.dev/icons?i=redis"/>
	<img src="https://skillicons.dev/icons?i=docker"/>
</div>

## Features

- **User CRUD Operations**: Create, Read, Update, and Delete users via API
- **RabbitMQ Integration**: Event-driven architecture for microservice communication
- **RESTful API**: Fully documented endpoints following OpenAPI standards
- **Scalable Design**: Ready for containerized deployment in cloud environments
* **Comprehensive User Management**: Add, edit, and delete users.
* **Powerful API**: Exposes RESTful APIs for user management.
* **RabbitMQ Support**: Listens to RabbitMQ queues for asynchronous operations.
* **Microservice-Ready**: Designed for use in microservice architectures.
* **Automatic Documentation**: Uses Swagger UI for automatic API documentation.
* **Data Validation**: Employs Pydantic for input/output data validation.
* **Persistence**: Utilizes a database for user data storage.

## API Endpoints

| Endpoint                           | Method | Description                        |
|------------------------------------|--------|------------------------------------|
| `/users`                           | POST   | Create new user                    |
| `/users`                           | GET    | List all users                     |
| `/users/id/{user_id}`              | GET    | Get user details by its id         |
| `/users/username/{username}`       | GET    | Get user details by its username   |
| `/users/public_key/{public_key}` | GET    | Get user details by its public key |
| `/users/{user_id}`                 | PUT    | Update user                        |
| `/users/{user_id}`                 | DELETE | Delete user                        |

## RabbitMQ Queues

The service listens to these queues:

- `user.create` - Process user creation events
- `user.update` - Handle user update events
- `user.delete` - Manage user deletion events

## Prerequisites

- Python 3.8+
- RabbitMQ server
- FastAPI dependencies

## Installation

1. Clone the repository:
   ```bash
   git clone +
   cd user-management
    ```
