from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_user = os.environ.get("MARIADB_USER")
db_password = os.environ.get("MARIADB_PASSWORD")
db_name = os.environ.get("MARIADB_DATABASE")

SQLALCHEMY_DB_URL = f'mariadb+pymysql://{db_user}:{db_password}@db:3306/{db_name}'

engine = create_engine(SQLALCHEMY_DB_URL, echo=True)
DBSession = sessionmaker(engine, autoflush=False)