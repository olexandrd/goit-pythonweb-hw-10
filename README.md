# goit-pythonweb-hw-08

## Setup

Run the following commands to set up the project environment:

```bash
docker-compose up -d
```

## Usage

Run the following command to start the project:

```bash
poetry shell && poetry install && alembic upgrade head && fastapi run

```

And open the following URL in your browser: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see the API documentation.
