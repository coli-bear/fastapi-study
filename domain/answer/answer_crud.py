from database import auto_commit
from domain.answer.answer_schema import AnswerCreateSchema
from models import Answer, Question
from sqlalchemy.orm import Session
from datetime import datetime


@auto_commit
def create_answer(db: Session, question: Question, answer: AnswerCreateSchema):
    db_answer = Answer(question=question, content=answer.content, create_date=datetime.now())
    db.add(db_answer)
