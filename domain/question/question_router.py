from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from domain.question.question_schema import QuestionSchema, QuestionCreateSchema, QuestionListSchema, \
    QuestionUpdateSchema, QuestionIdentifierSchema
from domain.user.user_router import get_current_user
from models import User
import domain.question.question_crud as question_crud

router = APIRouter(prefix="/api/question")


@router.get("/list", response_model=QuestionListSchema)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    total, _question_list = question_crud.question_list(db=db, skip=page * size, limit=size)

    return {
        "total": total,
        "questions": _question_list
    }


@router.get("/detail/{question_id}", response_model=QuestionSchema)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    return question_crud.question_detail(question_id=question_id, db=db)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def question_create(_question: QuestionCreateSchema,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.question_create(db=db, question=_question, user=current_user)


@router.put("/update", status_code=status.HTTP_200_OK)
def question_update(_question_update: QuestionUpdateSchema,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question = question_crud.question_detail(question_id=_question_update.question_id, db=db)

    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="질문을 찾을 수 없습니다.")

    if not question.is_owner(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다. 질문 작성자만 수정할 수 있습니다.")

    question_crud.update_question(question=question, question_update=_question_update, db=db)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(question_id: QuestionIdentifierSchema,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question = question_crud.question_detail(question_id=question_id.question_id, db=db)
    if not question:
        return

    if not question.is_owner(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다. 질문 작성자만 삭제할 수 있습니다.")

    question_crud.delete_question(question=question, db=db)
