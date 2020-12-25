import pytest
import docker
import socket
import time
from psycopg2 import OperationalError
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker


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


@pytest.yield_fixture(scope='function')
def postgres_db():
    client = docker.from_env()
    client.containers.run(
        image='postgres',
        name='test_managers',
        ports={'5432/tcp': 5433},
        auto_remove=True,
        environment=["POSTGRES_PASSWORD=postgres", "POSTGRES_DB=test_managers"],
        detach=True
    )
    print('container run')
    yield client
    client.containers.get('test_managers').stop()
    print('container stop')


def test_db(postgres_db):
    if ping_db():
        for _ in range(10):
            try:
                SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@localhost:5433/test_managers"
                engine = create_engine(SQLALCHEMY_DATABASE_URL)
                session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
                file = open('tests/filldb.sql')
                escaped_sql = sqlalchemy.text(file.read())
                engine.execute(escaped_sql)
                print('DB created')
                break
            except Exception as e:
                print('cant connect\n' + str(e))
                time.sleep(1)
    else:
        print('Cant connect to db')
    time.sleep(10)