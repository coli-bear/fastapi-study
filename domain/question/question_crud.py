from datetime import datetime

from database import auto_commit
from domain.question.question_schema import QuestionCreateSchema
from models import Question
from sqlalchemy.orm import Session


def question_list(db: Session):
    return db.query(Question).order_by(Question.create_date.desc()).all()


def question_detail(db: Session, question_id: int):
    return db.query(Question).get(question_id)


@auto_commit
def question_create(db: Session, question: QuestionCreateSchema):
    question = Question(subject=question.subject, content=question.content, create_date=datetime.now())
    db.add(question)
