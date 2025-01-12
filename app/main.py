import uuid
from datetime import datetime
from fastapi import FastAPI, Depends
from sqlmodel import insert, select, update

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.factory.problem import ProblemFactory
from app.managers.test_manager import TestManager
from app.schemas import (
    TestPaper, 
    GetPaperResponse, 
    PaperStore, 
    UserDTO, 
    UType, 
    Paper, 
    Text,
    PostSubmitResponse
)

from app.deps import Session, get_db

admin = UserDTO(
    id=uuid.UUID("949ac3fa-7967-43e2-8029-dd14a03ac8cd"), 
    name="admin"
)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/api/paper", response_model=GetPaperResponse)
async def get_paper(db: Session = Depends(get_db)):
    at_factory = ProblemFactory(db_session=db)
    published_version = (
        TestManager(user=admin)
        .publish_paper(at_factory)   
    )
    test_version = published_version.to_test_version()

    namespace = (published_version.binded.id, published_version.id)
    PaperStore.put(
        db, 
        namespace, 
        0,
        published_version.model_dump(mode="json")
    )

    return GetPaperResponse(paper = test_version)


@app.post("/api/submit", response_model=PostSubmitResponse)
async def submit_paper(test_paper: TestPaper, db: Session = Depends(get_db)):
 
    namespace = (test_paper.binded.id, test_paper.id)
    
    paper_json = PaperStore.get(db, namespace, 0) # type: ignore
    to_published_version = (
        Paper.model_validate(paper_json)
        .model_validate_to_end()
    )
    changed_paper = test_paper.apply_changes(to_published_version)

    
    PaperStore.put(
        db, 
        namespace, 
        0,
        changed_paper.model_dump(mode="json")
    )

    score = changed_paper.calculate_score()

    return PostSubmitResponse(
        score=score,
        user=changed_paper.binded
    )


@app.get("/api/analyze", response_model=PostSubmitResponse)
async def analyze(db: Session = Depends(get_db)):
    
    a = uuid.UUID("949ac3fa-7967-43e2-8029-dd14a03ac8cd")
    searched = PaperStore.search(db, namespace=(a,))
    print(searched)
