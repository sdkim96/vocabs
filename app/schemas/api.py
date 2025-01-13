import uuid

from pydantic import BaseModel, Field
from typing import List
from app.schemas import APIStatus, TestPaper, UserDTO
from app.schemas.test_paper import Paper

class BaseResponse(BaseModel):
    request_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    status: APIStatus = APIStatus.SUCCESS

class GetPaperResponse(BaseResponse):
    paper: TestPaper

class PostSubmitResponse(BaseResponse):
    score: int
    user: UserDTO

class GetResultResponse(BaseResponse):
    papers: List[Paper]
    