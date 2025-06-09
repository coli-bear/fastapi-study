from sqlalchemy.orm import Session
from starlette import status
from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from domain.user import user_schema
from domain.user import user_crud

router = APIRouter(prefix="/api/user")


@router.post("/create", status_code=status.HTTP_201_CREATED)
def user_create(_user_create: user_schema.UserCreateSchema, db: Session = Depends(get_db)):
    user = user_crud.exists_user(db=db, username=_user)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, _user=_user)
