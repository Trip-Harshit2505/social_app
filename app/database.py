from sqlmodel import SQLModel, create_engine, Session
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# POSTGRESQL_URL = "postgres://<username>:<password>@<ip-address/hostname>/<database_name"

DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(DATABASE_URL)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='05HA221325',cursor_factory=RealDictCursor)
#         curr = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(3)