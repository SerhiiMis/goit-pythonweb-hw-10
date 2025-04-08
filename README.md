# Contacts API

A simple asynchronous REST API for managing contacts, built with FastAPI, SQLAlchemy, PostgreSQL, and Pydantic.

## Features

- Create, read, update, and delete contacts
- Search contacts by first name, last name, or email
- Get contacts with upcoming birthdays in the next 7 days
- Swagger and ReDoc documentation
- Environment-based configuration using `.env`

## Technologies

- Python 3.12+
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- asyncpg
- Pydantic v2
- Uvicorn
- python-dotenv

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SerhiiMis/goit-pythonweb-hw-08.git
cd goit-pythonweb-hw-08
```

### 2. Create and configure `.env`

Create a `.env` file in the root directory based on `.example.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/contacts_db
```

Make sure PostgreSQL is running and the `contacts_db` database is created.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi sqlalchemy asyncpg psycopg2-binary uvicorn python-dotenv pydantic[email]
```

### 4. Run the application

```bash
createdb contacts_db
uvicorn app.main:app --reload
```

### 5. Open API docs

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Environment Files

- `.env` — used to store environment variables (e.g., DB credentials). **Do not commit this file.**
- `.example.env` — sample file to show required environment variables.
