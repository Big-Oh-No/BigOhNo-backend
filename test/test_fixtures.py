import pytest
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.db import get_db, Base
from fastapi.testclient import TestClient
from app.models import user_model
from app.main import app

SQL_ALCHEMY_DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
test_engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

Test_SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=test_engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.expunge_all()
            session.close()

    client = TestClient(app)
    app.dependency_overrides[get_db] = override_get_db
    yield client

@pytest.fixture
def token():
    return "korse"

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_verified_user(session):
    user_data = [
        {
            "email": "student@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "bio": "I am a second year student.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.Gender.male,
            "pronouns": "He/Him",
            "role": user_model.Role.student,
            "verified": True
        },
        {
            "email": "teacher@gmail.com",
            "first_name": "James",
            "last_name": "Potter",
            "bio": "I am a professor.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.Gender.male,
            "pronouns": "He/Him",
            "role": user_model.Role.teacher,
            "verified": True
        },
        {
            "email": "admin@gmail.com",
            "first_name": "Dave",
            "last_name": "Madland",
            "bio": "I am Admin.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.Gender.male,
            "pronouns": "He/Him",
            "role": user_model.Role.admin,
            "verified": True
        },
    ]

    def create_user(user_data):
        return user_model.User(**user_data)
    

    user_map = map(create_user, user_data)
    users = list(user_map)
    session.add_all(users)
    session.commit()
    users_list = session.query(user_model.User).all()
    return users_list



@pytest.fixture
def test_unverified_user(session):
    user_data = [
        {
            "email": "student1@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "bio": "I am a second year student.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.Gender.male,
            "pronouns": "He/Him",
            "role": user_model.Role.student,
            "verified": False
        },
        {
            "email": "teacher1@gmail.com",
            "first_name": "James",
            "last_name": "Potter",
            "bio": "I am a professor.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.Gender.male,
            "pronouns": "He/Him",
            "role": user_model.Role.teacher,
            "verified": False
        },
        {
            "email": "admin1@gmail.com",
            "first_name": "Dave",
            "last_name": "Madland",
            "bio": "I am Admin.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.Gender.male,
            "pronouns": "He/Him",
            "role": user_model.Role.admin,
            "verified": False
        },
    ]

    def create_user(user_data):
        return user_model.User(**user_data)
    

    user_map = map(create_user, user_data)
    users = list(user_map)
    session.add_all(users)
    session.commit()
    users_list = session.query(user_model.User).all()
    return users_list
