import datetime

from pydantic import BaseModel


class QuestionSchema(BaseModel):
    id: int
    subject: str
    content: str | None = None
    create_date: datetime.datetime
