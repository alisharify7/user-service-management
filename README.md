# User Management Microservice

A FastAPI-based microservice for user management with RabbitMQ event integration, providing RESTful APIs and message queue support for distributed systems.

## Features

- **User CRUD Operations**: Create, Read, Update, and Delete users via API
- **RabbitMQ Integration**: Event-driven architecture for microservice communication
- **RESTful API**: Fully documented endpoints following OpenAPI standards
- **Scalable Design**: Ready for containerized deployment in cloud environments

## API Endpoints

| Endpoint          | Method | Description                     |
|-------------------|--------|---------------------------------|
| `/users`          | POST   | Create new user                 |
| `/users`          | GET    | List all users                  |
| `/users/{user_id}`| GET    | Get user details                |
| `/users/{user_id}`| PUT    | Update user                     |
| `/users/{user_id}`| DELETE | Delete user                     |

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