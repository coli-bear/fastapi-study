from models import Question
from sqlalchemy.orm import Session


def question_list(db: Session):
    return db.query(Question).order_by(Question.create_date.desc()).all()


def question_detail(db: Session, question_id: int):
    return db.query(Question).get(question_id)
