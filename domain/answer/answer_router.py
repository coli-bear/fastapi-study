from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from database import get_db
from sqlalchemy.orm import Session

from domain.answer.answer_schema import AnswerCreateSchema, AnswerUpdateSchema, AnswerSchema, AnswerIdentifierSchema
from domain.question import question_crud
from domain.answer import answer_crud
from domain.user.user_router import get_current_user

from models import User

router = APIRouter(prefix="/api/answer")


@router.post("/create/{question_id}", status_code=status.HTTP_201_CREATED)
def create_answer(question_id: int,
                  _answer_create: AnswerCreateSchema,
                  db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    _question = question_crud.question_detail(db, question_id)
    if not _question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="질문을 찾을 수 없습니다.")
    answer_crud.create_answer(db, question=_question, answer=_answer_create, user=user)


@router.get("/detail/{answer_id}", response_model=AnswerSchema)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = answer_crud.get_answer_by_id(db, answer_id=answer_id)
    return answer

@router.put("/update", status_code=status.HTTP_200_OK)
def update_answer(answer_update: AnswerUpdateSchema,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    answer = answer_crud.get_answer_by_id(db, answer_update.answer_id)
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="답변을 찾을 수 없습니다.")

    if not answer.is_owner(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다. 답변 작성자만 수정할 수 있습니다.")

    answer_crud.update_answer(db=db, answer=answer, answer_update=answer_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: AnswerIdentifierSchema,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    answer = answer_crud.get_answer_by_id(db, answer_id.answer_id)
    if not answer:
        return

    if not answer.is_owner(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다. 답변 작성자만 삭제할 수 있습니다.")

    answer_crud.delete_answer(db=db, answer=answer)