import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_USER = os.getenv('PG_USER', 'postgres')
DB_PASS = os.getenv('PG_PASS', 'postgres')
DB_HOST = os.getenv('PG_HOST', 'localhost')
DB_NAME = os.getenv('PG_DB', 'postgres')

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
