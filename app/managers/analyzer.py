import random
from sqlmodel import select, Session, values
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas import (
    PaperStore, 
    User, 
    Paper, 
    Text
)

class Evaluation(BaseModel):
    score: int
    total: int
    percentage: float

class TestAnalyzer:

    def __init__(
        self,
        db_session: Session,
        user: User,
        paper: Paper
    ) -> None:
        
        self.db_session = db_session
        self.user = user
        self.paper = paper
    
    def get_papers_by_user(self) -> List[Paper]:
        """ 학생이 푼 문제지들을 가져옴 """

        with self.db_session as session:
            stmt = (
                select(PaperStore.value)
                .where(PaperStore.prefix == str(self.user.id))
            )
            papers = session.exec(stmt).fetchall()
        
        user_papers = []
        for paper in papers:
            casted = Paper.model_validate(paper)
            casted.model_validate_to_end()

            user_papers.append(casted)
        
        return user_papers

    def get_papers_by_paper(self) -> List[Paper]:
        """ 같은 문제지들을 가져옴"""
        
        with self.db_session as session:
            stmt = (
                select(PaperStore.value)
                .where(PaperStore.key == str(self.paper.id))
            )
            papers = session.exec(stmt).fetchall()
        
        same_papers = []
        for paper in papers: # type: ignore
            casted = Paper.model_validate(paper)
            casted.model_validate_to_end()

            same_papers.append(casted)

        return same_papers
    
    def evaluate(self) -> Evaluation:
        """ 학생을 평가함"""
        return Evaluation()