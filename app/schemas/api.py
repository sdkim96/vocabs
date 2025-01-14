import uuid

from pydantic import BaseModel, Field
from typing import List
from app.schemas import APIStatus, Paper, UserDTO, TestPaper
from app.schemas.test_paper import PaperMeta

class BaseResponse(BaseModel):
    request_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    status: APIStatus = APIStatus.SUCCESS

class GetTestPaperResponse(BaseResponse):
    paper: TestPaper

class GetPaperResponse(BaseResponse):
    paper: Paper

class PostSubmitResponse(BaseResponse):
    score: int
    user: UserDTO

class GetResultResponse(BaseResponse):
    papers: List[PaperMeta]
    
class GetStudentsResponse(BaseResponse):
    students: List[UserDTO]