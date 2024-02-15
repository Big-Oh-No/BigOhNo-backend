## Tech Stack
In this open source project, we use FastAPI for the backend with PostgresSQL for the database with SQLAlcemy ORM to interact with the database in addition to Alembic for database migration.

### Build Command
```sh
pip install -r requirements.txt && alembic upgrade head
```

### Deploy Command
```sh
uvicorn app.main:app --host 0.0.0.0 --reload
```

---

### Running Alembic Migrations
To run database migrations, run
```sh
alembic revision -autogenerate -m "REVISION MESSAGE"
```