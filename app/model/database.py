from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PW")
db_name = os.environ.get("DB_NAME")
db_host = os.environ.get("DB_HOST")

SQLALCHEMY_DB_URL = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'

engine = create_engine(SQLALCHEMY_DB_URL, echo=True)
DBSession = sessionmaker(engine, autoflush=False)