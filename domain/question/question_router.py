from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from domain.question.question_schema import QuestionSchema

import domain.question.question_crud as question_crud

router = APIRouter(prefix="/question")


@router.get("/", response_model=list[QuestionSchema])
def question_list(db: Session = Depends(get_db)):
    return question_crud.question_list(db=db)
