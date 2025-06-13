from datetime import datetime

from sqlalchemy.orm import Session

from database import auto_commit
from domain.answer.answer_schema import AnswerCreateSchema, AnswerUpdateSchema
from models import Answer, Question, User


@auto_commit
def create_answer(db: Session, question: Question,
                  answer: AnswerCreateSchema,
                  user: User):
    db_answer = Answer(question=question,
                       content=answer.content,
                       create_date=datetime.now(),
                       user=user)
    db.add(db_answer)


def get_answer_by_id(db: Session, answer_id: int):
    return db.query(Answer).filter(Answer.id == answer_id).first()


@auto_commit
def update_answer(db: Session, answer: Answer, answer_update: AnswerUpdateSchema):
    answer.content = answer_update.content
    answer.modify_date = datetime.now()
    db.add(answer)


@auto_commit
def delete_answer(db: Session, answer: Answer):
    db.delete(answer)
