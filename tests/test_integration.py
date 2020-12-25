import pytest
import docker
import socket
import time
import sqlalchemy
import sys
sys.path = ['', '..'] + sys.path[1:]

from app.models.user.db_model import User
from app.models.project.db_model import Project
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def ping_db():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout = 1
    for _ in range(10):
        try:
            s.connect(('localhost', 5433))
            s.shutdown(timeout)
            return True
        except ConnectionRefusedError:
            time.sleep(timeout)
    else:
        return False


@pytest.fixture(scope='session')
def postgres_container():
    client = docker.from_env()
    client.containers.run(
        image='postgres',
        name='test_managers',
        ports={'5432/tcp': 5433},
        auto_remove=True,
        environment=["POSTGRES_PASSWORD=postgres", "POSTGRES_DB=test_managers"],
        detach=True
    )
    yield client
    client.containers.get('test_managers').stop()


@pytest.fixture(scope='session')
def postgres_session():
    if ping_db():
        for _ in range(10):
            try:
                SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@localhost:5433/test_managers"
                engine = create_engine(SQLALCHEMY_DATABASE_URL)
                session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
                file = open('tests/filldb.sql')
                escaped_sql = sqlalchemy.text(file.read())
                engine.execute(escaped_sql)
                yield session
                break
            except Exception as e:
                time.sleep(1)
    else:
        print('Cant connect to db')
    session.close()


def test_db(postgres_container, postgres_session):
    assert len(postgres_session.query(User).all()) == 19
    assert postgres_session.query(User).filter(User.id == 1).first().name == 'Anton'


def test_db2(postgres_session):
    assert len(postgres_session.query(Project).all()) == 4


def test_managers_not_auth():
    response = client.get('/managers')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'


def test_managers_owner(postgres_session):
    user_name = postgres_session.query(User).filter(User.id == 1).first().name
    user_jwt = client.post(f'/login/access-token?username={user_name}').json()['access_token']
    response = client.get('/managers', headers={'Authorization': f'Bearer {user_jwt}'})
    assert response.status_code == 200
    project_list = ('Umbrella', 'Werwolf')
    for project in project_list:
        assert project in response.json()

    managers_list = ('Alena', 'Alisa', 'Almeria', 'Junk')
    assert len(response.json()['Umbrella']) == 4
    for manager in managers_list:
        assert manager in response.json()['Umbrella']

    managers_list = ('Epitone', 'Minami', 'Krabzr')
    assert len(response.json()['Werwolf']) == 4
    for manager in managers_list:
        assert manager in response.json()['Werwolf']

    response = client.get('/managers?q=1', headers={'Authorization': f'Bearer {user_jwt}'})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert 'Umbrella' in response.json()
    assert 'Werwolf' not in response.json()

    response = client.get('/managers?q=2', headers={'Authorization': f'Bearer {user_jwt}'})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert 'Umbrella' not in response.json()
    assert 'Werwolf' in response.json()

    response = client.get('/managers?q=3', headers={'Authorization': f'Bearer {user_jwt}'})
    assert response.status_code == 200
    assert len(response.json()) == 0
    assert 'Umbrella' not in response.json()
    assert 'Werwolf' not in response.json()


def test_managers_employee(postgres_session):
    user_name = postgres_session.query(User).filter(User.id == 2).first().name
    user_jwt = client.post(f'/login/access-token?username={user_name}').json()['access_token']
    response = client.get('/managers', headers={'Authorization': f'Bearer {user_jwt}'})

    project_list = ('Umbrella', 'Werwolf')
    for project in project_list:
        assert project in response.json()

    managers_list = ('Alisa', 'Almeria', 'Junk')
    assert len(response.json()['Umbrella']) == 3
    for manager in managers_list:
        assert manager in response.json()['Umbrella']

    assert len(response.json()['Werwolf']) == 1
    assert 'Alena' in response.json()['Werwolf']
