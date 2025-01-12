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
    
    def analyze(self, papers: List[Paper]):
        """ 문제지의 시퀀스를 분석함 """
        
        for paper in papers:
            owner = paper.get_owner_name()
            score = paper.calculate_score()

            print(f"{owner}의 점수는 {score}점 입니다.")
        
        return papers


    def get_papers_by_user(self) -> List[Paper]:
        """ 같은 학생이 푼 서로다른 문제지들을 가져옴 """

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