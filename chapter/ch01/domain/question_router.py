from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import Question

from domain.question_schema import QuestionSchema

import domain.question_crud as question_crud

router = APIRouter(prefix="/question")


# @router.get("/list")
# def question_list():
#     with get_db() as db:
#         _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#
#     return _question_list

@router.get("/list", response_model=list[QuestionSchema])
def question_list(db: Session = Depends(get_db)):
    return question_crud.question_list(db=db)
