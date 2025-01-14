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
    ) -> None:
        
        self.db_session = db_session
    
    def analyze(self, papers: List[Paper]):
        """ 문제지의 시퀀스를 분석함 """
        
        for paper in papers:
            owner = paper.get_owner_name()
            score = paper.calculate_score()

            print(f"{owner}의 점수는 {score}점 입니다.")
        
        return papers
    
    
    def evaluate(self) -> Evaluation:
        """ 학생을 평가함"""
        return Evaluation()