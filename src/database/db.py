from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DB_URL = "postgresql://admin:admin@localhost:5432/rest_api"

engine = create_engine(DB_URL)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
