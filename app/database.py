from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import DictCursor

from app.config import settings
import time


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Relational Dependency

def connect_db():
    try:
        conn = psycopg2.connect(
            host='localhost', 
            port=5432,
            dbname='apidev', 
            user='postgres',  
            password='passworD98!',
            cursor_factory=DictCursor
            )
        cursor = conn.cursor()
        print("Database connection was successful!")
    except Exception as error:
        print("Database connection failed!")
        print("Error: ", error)
        time.sleep(2)

    return conn, cursor


conn, cursor = connect_db()

# ORM Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()