from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import auto_commit
from domain.user.user_schema import UserCreateSchema
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auto_commit
def create_user(db: Session, _user: UserCreateSchema):
    _crypted_password = pwd_context.hash(_user.password)
    _user = User(username=_user.username, password=_crypted_password, email=_user.email)
    db.add(_user)


def exists_user(db:Session, user: UserCreateSchema):
    return db.query(User).filter(User.username == user.username or User.email == user.email).first()
