from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from domain.question.question_schema import QuestionSchema

import domain.question.question_crud as question_crud

router = APIRouter(prefix="/api/question")


@router.get("/list", response_model=list[QuestionSchema])
def question_list(db: Session = Depends(get_db)):
    return question_crud.question_list(db=db)


@router.get("/detail/{question_id}", response_model=QuestionSchema)
def question_detail(question_id: int,db: Session = Depends(get_db)):
    return question_crud.question_detail(question_id=question_id, db=db)
