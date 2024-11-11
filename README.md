
# Temple8

This FastAPI template provides a ready-to-use Docker Compose setup for a modern, scalable web application. It includes a FastAPI app, Celery workers, and a **gRPC** service, with **Postgres** as the database and **RabbitMQ** as the broker for Celery tasks. The application uses **Gunicorn** with Uvicorn workers to serve FastAPI, ensuring efficient handling of requests.

## Features
- **FastAPI** for creating RESTful APIs
- **Gunicorn** with Uvicorn workers for serving the app
- **SQLAlchemy (async)** with Postgres as the ORM and database
- **Celery** for background task processing, using RabbitMQ as the broker
- **CircuitBreaker** for fault-tolerant API calls
- **Alembic** for managing database migrations
- **Docker Compose** for easy service orchestration and deployment

## Requirements
- **Docker** and **Docker Compose**
- **Python 3.11+**

## Setup

### 1. Configure Environment Variables

Create `.env` files in the root directory and `bakery_grpc` folder with the required environment variables:

- **`.env`** (root): Holds configuration for the FastAPI app, database, and Celery broker.
- **`bakery_grpc/.env`**: Holds configuration for the gRPC bakery service.

Ensure all sensitive and environment-specific configurations (such as database credentials) are properly set in these files.

### 2. Running with Makefile

This project includes a `Makefile` with commands to streamline development:

- **Start all services with Docker**:
  ```bash
  make run-container
  ```
- **Stop all services**:
  ```bash
  make kill-container
  ```
- **Run services locally** (without Docker):
  ```bash
  make run-local
  ```

To see all available Makefile commands, use:
```bash
make help
```
### Explore the endpoints

-   To play around with the APIs, go to the following link on your browser:

    ```sh
    http://localhost:5001/docs
    ```

-   Press the `authorize` button on the right and add _username_ and _password_. The APIs
    use OAuth2 (with hashed password and Bearer with JWT) based authentication. In this
    case, the username and password is `ubuntu` and `debian` respectively.

    Clicking the `authorize` button and you're all set.


## Project Structure

The application is modular and organized for scalability and clarity. Key modules include:

### Configuration (`app/core/*`)
- **`app/core/config.py`**: Centralizes configuration settings.
- **`app/core/celery.py`**: Configures the Celery worker.
  
### API Modules (`app/apis/*`)
- **Structure**: Each module in `app/apis/` follows a standardized pattern:
  - **`models`**: Defines Pydantic models for data validation.
  - **`srv`**: Contains business logic and service functions.
  - **`routes`**: Defines FastAPI routers that use the services.

### Database (`app/db/*`)
- **`db.py`**: Contains the core database connection setup for Postgres.
- **Alembic**: The `app/db` folder includes schemas used by Alembic to generate and apply database migrations.

To create a new migration after modifying models, run:
```bash
alembic revision --autogenerate -m "your migration message"
```
Then, apply the migration with:
```bash
alembic upgrade head
```

### Dependencies (`app/dependencies/*`)
- External dependencies and services are kept in `app/dependencies`.
- **gRPC Bakery Service**: The `bakery_grpc` directory provides a client example for using gRPC to interact with the bakery service.

### Testing (`app/tests/*`)
- Test cases are organized under `app/tests`.
- Run tests with:
  ```bash
  make test
  ```
  This uses **pytest** for a streamlined testing experience.

## Development and Deployment

### Running with Docker Compose

To start all services, run:
```bash
docker compose up --build -d
```

This command will start:
- The FastAPI application server with Gunicorn and Uvicorn workers
- The Celery worker
- The gRPC bakery service
- PostgreSQL and RabbitMQ

To stop and remove all running containers:
```bash
docker compose down
```

### Running Migrations on Start

The Docker configuration automatically applies Alembic migrations each time the `app` service starts. This is handled in the `docker compose.yml` file:
```yaml
entrypoint:
  - /bin/sh
  - -c
  - |
    alembic upgrade head &&
    gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker -b 0.0.0.0:5001
```

## Accessing the API

With the app running, you can access the FastAPI documentation at:
- **Swagger UI**: [http://localhost:5001/docs](http://localhost:5001/docs)
- **ReDoc**: [http://localhost:5001/redoc](http://localhost:5001/redoc)

## License

MIT License. See LICENSE for details.
