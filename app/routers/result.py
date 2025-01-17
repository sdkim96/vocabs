import uuid
from typing import Annotated
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends, Query

from app.managers.publisher import Publisher
from app.schemas import (
    PaperStore, 
    User,
    Paper,
    UType,

    GetPaperResponse,
    GetResultResponse,
    StoreSearchOption,
)

from app.deps import Session, get_db, get_current_user

result_r = APIRouter()

@result_r.get("/specific", response_model=GetPaperResponse)
async def get_result_of_paer(
    paper_id: Annotated[uuid.UUID, Query()],
    test_id: Annotated[uuid.UUID, Query()],
    me: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    namespace = (me.id, paper_id)
    
    return GetPaperResponse(
        paper=(
            Paper
            .model_validate(
                PaperStore.get(db, namespace, test_id)
            )
            .model_validate_to_end()
        ) # type: ignore
    )


@result_r.get("/meta/me", response_model=GetResultResponse)
async def get_my_result_only_meta(
    me: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
):
    
    publisher = Publisher()
    papers = publisher.get_papers_by_user(db, me, option=StoreSearchOption.META)

    return GetResultResponse(
        papers=papers # type: ignore
    )


@result_r.get("/meta/all", response_model=GetResultResponse)
async def get_student_result_only_meta(
    student_id: Annotated[uuid.UUID, Query()], 
    my: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if my.user_type not in [UType.TEACHER, UType.ADMIN]:
        raise HTTPException(status_code=403, detail="You are not a teacher")
    
    student = User.get_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    publisher = Publisher()
    papers = publisher.get_papers_by_user(db, student, option=StoreSearchOption.META)

    return GetResultResponse(
        papers=papers # type: ignore
    )