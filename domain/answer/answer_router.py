from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from database import get_db
from sqlalchemy.orm import Session

from domain.answer.answer_schema import AnswerCreateSchema
from domain.question import question_crud
from domain.answer import answer_crud
from domain.user.user_router import get_current_user

from models import User

router = APIRouter(prefix="/api/answer")


@router.post("/create/{question_id}", status_code=status.HTTP_201_CREATED)
def create_answer(question_id: int,
                  _answer_create: AnswerCreateSchema,
                  db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    _question = question_crud.question_detail(db, question_id)
    if not _question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="질문을 찾을 수 없습니다.")
    answer_crud.create_answer(db, question=_question, answer=_answer_create, user=user)
