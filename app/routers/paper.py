import uuid
from fastapi import APIRouter
from fastapi import Depends

from app.schemas import (
    UserDTO,
    User,
    GetTestPaperResponse,
    PostSubmitResponse,
    TestPaper,
    PaperStore,
    Paper
)
from app.deps import (
    Session, 
    get_db, 
    get_current_user
)
from app.factory.problem import ProblemFactory
from app.managers.publisher import Publisher

paper_r = APIRouter()

@paper_r.get("/paper", response_model=GetTestPaperResponse)
async def get_paper(me: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    this_user = UserDTO(
        id=me.id, 
        name=me.name,
        user_name=me.user_name,
        user_nickname=me.user_nickname,
    )
    at_factory = ProblemFactory(db_session=db)
    published_version = (
        Publisher(target_user=this_user)
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

    return GetTestPaperResponse(paper = test_version)


@paper_r.post("/submit", response_model=PostSubmitResponse)
async def submit_paper(test_paper: TestPaper, me: User = Depends(get_current_user), db: Session = Depends(get_db)):
 
    namespace = (test_paper.binded.id, test_paper.paper_id)
    
    paper_json = PaperStore.get(db, namespace, test_paper.test_id) # type: ignore
    to_published_version = (
        Paper
        .model_validate(paper_json)
        .model_validate_to_end()
    )
    changed_paper = test_paper.apply_changes(to_published_version)

    
    PaperStore.put(
        db, 
        namespace, 
        str(test_paper.test_id),
        changed_paper.model_dump(mode="json")
    )

    score = changed_paper.calculate_score()

    return PostSubmitResponse(
        score=score,
        user=changed_paper.binded
    )