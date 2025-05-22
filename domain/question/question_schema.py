import datetime

from pydantic import BaseModel

from domain.answer.answer_schema import AnswerSchema


class QuestionSchema(BaseModel):
    id: int
    subject: str
    content: str | None = None
    create_date: datetime.datetime
    answers: list[AnswerSchema] = []
