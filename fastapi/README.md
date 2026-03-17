# FastAPI Todo API

A REST API built with FastAPI and PostgreSQL for managing todo items

## Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM for database interaction
- **Alembic** - Database migrations
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **psycopg2** - PostgreSQL adapter

## Project Structure

```
fastapi/
├── main.py               # App entry point
├── alembic.ini           # Alembic config
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
├── alembic/
│   ├── env.py
│   └── versions/         # Migration files
└── app/
    ├── config/
    │   └── app_config.py
    ├── database/
    │   └── db.py         # DB connection and session
    ├── models/
    │   └── todo.py       # SQLAlchemy and Pydantic models
    └── routes/
        └── todo.py       # Todo endpoints
```

## Setup

### 1. Clone the repository and navigate to the project folder

```bash
cd fastapi
```

### 2. Create and activate a virtual environment

```bash
uv venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/yourdbname
```

### 5. Run database migrations

```bash
uv run alembic upgrade head
```

### 6. Start the server

```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint   | Description        |
|--------|------------|--------------------|
| GET    | /          | Health check       |
| GET    | /test-db   | Test DB connection |
| GET    | /todo/     | List all todos     |
| POST   | /todo/     | Create a todo      |

## Example Request

### Create a Todo

```http
POST /todo/
Content-Type: application/json

{
  "content": "Buy groceries",
  "is_completed": false
}
```

### Response

```json
{
  "message": "todo created",
  "item": {
    "id": 1,
    "content": "Buy groceries",
    "is_completed": false
  }
}
```

## Interactive Docs

FastAPI provides auto-generated documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
