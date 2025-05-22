from models import Question
from sqlalchemy.orm import Session


def question_list(db: Session):
    return db.query(Question).order_by(Question.create_date.desc()).all()
