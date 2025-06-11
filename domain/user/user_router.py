from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from sqlalchemy.orm import Session
from starlette import status
from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from domain.user import user_schema
from domain.user import user_crud
from domain.user.user_schema import UserTokenSchema

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c"
ALGORITHM = "HS256"

router = APIRouter(prefix="/api/user")


@router.post("/create", status_code=status.HTTP_201_CREATED)
def user_create(_user_create: user_schema.UserCreateSchema, db: Session = Depends(get_db)):
    user = user_crud.exists_user(db=db, user=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, _user=_user_create)


@router.post("/signin", response_model=UserTokenSchema)
def user_signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db=db, username=form_data.username)
    if not user or not user_crud.pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자 이름 또는 비밀번호가 잘못되었습니다.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # JWT 토큰 생성
    data = {
        "sub": user.username,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return UserTokenSchema(access_token=access_token, token_type="bearer", username=user.username)
