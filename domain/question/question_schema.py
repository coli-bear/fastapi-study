import datetime

from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import AnswerSchema
from domain.user.user_schema import UserSchema


class QuestionSchema(BaseModel):
    id: int
    subject: str
    content: str | None = None
    create_date: datetime.datetime
    answers: list[AnswerSchema] = []
    user: UserSchema | None


class QuestionCreateSchema(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, value: str):
        if not value or not value.strip():
            raise ValueError("빈 값은 허용되지 않습니다..")
        return value


class QuestionListSchema(BaseModel):
    total: int = 0
    questions: list[QuestionSchema] = []
