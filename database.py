from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# TODO : Move to environment variable
DATABASE_SOURCE = "postgresql://postgres:postgres@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_SOURCE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

Base.metadata = MetaData(naming_convention = naming_convention)

def __kwargs_session_get(kwargs):
    for key, value in kwargs.items():
        if isinstance(value, Session):
            return value
    return None


def __args_session_get(args):
    for arg in args:
        if isinstance(arg, Session):
            return arg
    return None


def __session_get(args, kwargs):
    db = __args_session_get(args)
    if db is None:
        db = __kwargs_session_get(kwargs)
    return db


def auto_commit(func):
    def wrapper(*args, **kwargs):
        try:
            db = __session_get(args, kwargs)
        except AttributeError:
            raise AttributeError('You need to define database session attribute')

        if db is None:
            raise AttributeError('You need to define database session attribute')
        try:
            result = func(*args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            db.rollback()
            raise e

    return wrapper


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
