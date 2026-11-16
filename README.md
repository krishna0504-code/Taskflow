# TaskFlow – Python Task Management REST API

TaskFlow is a backend project built with **Python and Flask**. It provides secure user registration/login and personal task management through RESTful endpoints. Each user can only access their own tasks.

## Features

- User registration and login
- Password hashing (Werkzeug)
- JWT-based authentication
- Create, read, update and delete tasks (CRUD)
- Task status and priority management
- Due dates and status filtering
- Pagination for task lists
- Input validation and JSON error responses
- SQLite database with SQLAlchemy ORM
- Docker support
- Automated API tests with pytest

## Technology stack

Python 3.12, Flask, Flask-SQLAlchemy, SQLite, Flask-JWT-Extended, REST API, Docker, pytest, Git.

## Run locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\\Scripts\\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. (Recommended) Copy `.env.example` to `.env` and set strong secrets. Load environment variables using your preferred method, or set them in your terminal.
5. Start the API:

   ```bash
   python run.py
   ```

The API runs at `http://localhost:5000`. Visit `/` or `/health` to check it.

## Run with Docker

```bash
docker compose up --build
```

The API will be available at `http://localhost:5000`. Docker Compose stores the SQLite database in a named volume.

## API endpoints

All task endpoints require this header after login:

`Authorization: Bearer <access_token>`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| POST | `/api/auth/register` | Register a user |
| POST | `/api/auth/login` | Login and receive JWT |
| POST | `/api/tasks` | Create a task |
| GET | `/api/tasks` | List your tasks |
| GET | `/api/tasks/<id>` | Get one task |
| PATCH | `/api/tasks/<id>` | Update a task |
| DELETE | `/api/tasks/<id>` | Delete a task |

Optional list parameters: `?status=pending&page=1&per_page=10`.

### Example requests

Register:

```json
{
  "username": "himanshu",
  "email": "himanshu@example.com",
  "password": "ChangeMe123!"
}
```

Login:

```json
{
  "identity": "himanshu",
  "password": "ChangeMe123!"
}
```

Create a task:

```json
{
  "title": "Complete Python project",
  "description": "Add tests and update README",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2026-12-01"
}
```

Valid statuses: `pending`, `in_progress`, `completed`.

Valid priorities: `low`, `medium`, `high`.

## Run tests

```bash
pytest -q
```

## Suggested manual test flow

1. Register a user using `/api/auth/register`.
2. Login using `/api/auth/login` and copy the `access_token`.
3. In Postman, add the Bearer token to the Authorization tab.
4. Create a task, list tasks, update a task, and delete a task.
5. Register a second user and verify that the first user's tasks are not visible.

## Project structure

```text
taskflow_python_backend/
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── __init__.py
│   └── models.py
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── README.md
```

## Before publishing

- Change all development secrets.
- Do not commit `.env` or database files.
- Add screenshots or a short Postman demo to your portfolio.
- Deploy only after configuring production secrets, HTTPS, and a production WSGI server.

## Resume description

**TaskFlow – Task Management REST API**
- Developed a Python Flask REST API with JWT authentication and CRUD operations for personal task management.
- Integrated SQLite with SQLAlchemy, input validation, task filtering and pagination; containerized the application using Docker and added automated tests with pytest.

**Note:** This is a portfolio project starter. Run the tests and manually verify the API in your environment before adding it to your resume.
