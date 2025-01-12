import uuid
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.factory.problem import ProblemFactory
from app.managers.test_manager import TestManager
from app.schemas import (
    TestPaper,  
    PaperStore, 
    UserDTO,
    UserCreate, 
    User,
    UserSignIn,
    Paper, 

    GetPaperResponse,
    PostSubmitResponse,
    Token
)

from app.deps import Session, get_db, get_current_user

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
async def get_paper(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    this_user = UserDTO(id=user.id, name=user.name)
    at_factory = ProblemFactory(db_session=db)
    published_version = (
        TestManager(user=this_user)
        .publish_paper(at_factory)   
    )
    test_version = published_version.to_test_version(test_id=uuid.uuid4())

    namespace = (published_version.binded.id, published_version.id)
    PaperStore.put(
        db, 
        namespace, 
        str(test_version.test_id),
        published_version.model_dump(mode="json")
    )

    return GetPaperResponse(paper = test_version)


@app.post("/api/submit", response_model=PostSubmitResponse)
async def submit_paper(test_paper: TestPaper, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
 
    namespace = (test_paper.binded.id, test_paper.paper_id)
    
    paper_json = PaperStore.get(db, namespace, test_paper.test_id) # type: ignore
    to_published_version = (
        Paper.model_validate(paper_json)
        .model_validate_to_end()
    )
    changed_paper = test_paper.apply_changes(to_published_version)

    
    PaperStore.put(
        db, 
        namespace, 
        str(test_paper.paper_id),
        changed_paper.model_dump(mode="json")
    )

    score = changed_paper.calculate_score()

    return PostSubmitResponse(
        score=score,
        user=changed_paper.binded
    )


@app.get("/api/analysis", response_model=PostSubmitResponse)
async def analyze(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    searched = PaperStore.search(db, namespace=(user.id,))
    print(searched)


@app.post("/api/sign_up", response_model=UserDTO)
async def sign_up(new_user: UserCreate, db: Session = Depends(get_db)):
    
    created = User.create(db, user=new_user)
    if created:
        return UserDTO(id=created.id, name=created.name)
    
@app.post("/api/sign_in", response_model=Token)
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    
    exist = User.get(db, form_data.username)

    if not exist:
        raise HTTPException(status_code=500, detail="User not found")
    
    if exist.verify(form_data.password):
        token = Token.new(exist)
        return token
    else:
        raise HTTPException(status_code=500, detail="Password not matched")


@app.get("/api/user/me", response_model=UserDTO)
async def get_me(user: User = Depends(get_current_user)):
    return UserDTO(id=user.id, name=user.name)