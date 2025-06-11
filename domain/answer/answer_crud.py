from database import auto_commit
from domain.answer.answer_schema import AnswerCreateSchema
from models import Answer, Question, User
from sqlalchemy.orm import Session
from datetime import datetime


@auto_commit
def create_answer(db: Session, question: Question,
                  answer: AnswerCreateSchema,
                  user: User):
    db_answer = Answer(question=question,
                       content=answer.content,
                       create_date=datetime.now(),
                       user=user)
    db.add(db_answer)
