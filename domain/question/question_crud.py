from datetime import datetime

from database import auto_commit
from domain.question.question_schema import QuestionCreateSchema
from models import Question, User
from sqlalchemy.orm import Session


def question_list(db: Session, skip: int = 0, limit: int = 10):
    _question_list = db.query(Question).order_by(Question.create_date.desc())
    return _question_list.count(), \
        _question_list \
            .offset(skip) \
            .limit(limit).all()


def question_detail(db: Session, question_id: int):
    return db.query(Question).get(question_id)


@auto_commit
def question_create(db: Session, question: QuestionCreateSchema, user: User):
    question = Question(subject=question.subject,
                        content=question.content,
                        create_date=datetime.now(),
                        user=user)
    db.add(question)
