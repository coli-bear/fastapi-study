from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from domain.question.question_schema import QuestionSchema, QuestionCreateSchema, QuestionListSchema
from domain.user.user_router import get_current_user
from models import User
import domain.question.question_crud as question_crud

router = APIRouter(prefix="/api/question")


@router.get("/list", response_model=QuestionListSchema)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    total, _question_list = question_crud.question_list(db=db, skip=page * size, limit=size)

    return {
        "total": total,
        "questions": _question_list
    }


@router.get("/detail/{question_id}", response_model=QuestionSchema)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    return question_crud.question_detail(question_id=question_id, db=db)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def question_create(_question: QuestionCreateSchema,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    question_crud.question_create(db=db, question=_question, user=user)
