import uuid
from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter
from fastapi import HTTPException, Depends, Query

from app.managers.publisher import Publisher
from app.schemas import (
    PaperStore, 
    User,
    Paper,
    UType,
    PaperMeta,

    GetPaperResponse,
    GetResultResponse,
    StoreSearchOption,
)

from app.deps import Session, get_db, get_current_user

result_r = APIRouter()

@result_r.get("/specific/me", response_model=GetPaperResponse)
async def get_my_result_of_paper(
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

@result_r.get("/specific", response_model=GetPaperResponse)
async def get_result_of_paper_of(
    student_id: Annotated[uuid.UUID, Query()],
    paper_id: Annotated[uuid.UUID, Query()],
    test_id: Annotated[uuid.UUID, Query()],
    me: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    namespace = (student_id, paper_id)
    
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
    papers = publisher.get_papers_by_user(db, me, option=StoreSearchOption.ALL)

    meta = []
    for paper in papers:

        target = paper.value
        target_paper =(
            Paper
            .model_validate(target)
            .model_validate_to_end()
        )

        score = target_paper.calculate_score()
        
        meta.append(
            PaperMeta(
                paper_id=paper.prefix.split(".")[-1],
                test_id=paper.key,
                created_at=paper.created_at if paper.created_at is not None else datetime.now(),
                updated_at=paper.updated_at if paper.updated_at is not None else datetime.now(),
                score=score
            )
        )

    return GetResultResponse(
        papers=meta # type: ignore
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
    papers: List[PaperStore] = publisher.get_papers_by_user(db, student, option=StoreSearchOption.ALL)
    
    meta = []
    for paper in papers:

        target = paper.value
        target_paper =(
            Paper
            .model_validate(target)
            .model_validate_to_end()
        )

        score = target_paper.calculate_score()
        
        meta.append(
            PaperMeta(
                paper_id=paper.prefix.split(".")[-1],
                test_id=paper.key,
                created_at=paper.created_at if paper.created_at is not None else datetime.now(),
                updated_at=paper.updated_at if paper.updated_at is not None else datetime.now(),
                score=score
            )
        )

    return GetResultResponse(
        papers=meta # type: ignore
    )