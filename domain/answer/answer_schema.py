from datetime import datetime
from pydantic import BaseModel, field_validator

from domain.user.user_schema import UserSchema

class AnswerIdentifierSchema(BaseModel):
    answer_id: int

    @field_validator('answer_id')
    def positive_id(cls, answer_id: int):
        if not answer_id or answer_id <= 0:
            raise ValueError("답변 ID는 양수여야 합니다.")
        return answer_id

class AnswerCreateSchema(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, content: str):
        print(content)
        if not content or not content.strip():
            raise ValueError("컨텐츠가 비어있거나 공백일 수 없습니다.")
        return content

class AnswerSchema(BaseModel):
    id: int
    content: str
    create_date: datetime
    user: UserSchema | None
    question_id: int

class AnswerUpdateSchema(AnswerIdentifierSchema, AnswerCreateSchema):
    pass