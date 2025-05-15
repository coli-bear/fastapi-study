from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_SOURCE = "postgresql://postgres:postgres@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_SOURCE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def auto_commit(func):
    def wrapper(*args, **kwargs):
        try:
            db = kwargs.get('db')
        except AttributeError:
            raise AttributeError('You need to define db attribute')

        try:
            result = func(*args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            db.rollback()
            raise e
    return wrapper