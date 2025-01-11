import random
import uuid
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLModelField
from sqlalchemy.dialects.postgresql import JSONB

from app.schemas.enum import Difficulty
from app.schemas.problem import Problem, QA, Text
from app.schemas.auth import User


class PaperStore(SQLModel, table=True):

    __table_args__ = {"extend_existing": True}

    prefix: str = SQLModelField(primary_key=True, nullable=False, description="Represents the doc's namespace")
    key: str = SQLModelField(primary_key=True, nullable=False, description="The unique key for the value")
    value: Dict = SQLModelField(sa_type=JSONB, nullable=False, description="The JSON value stored in the table")  # dict로 변경
    created_at: Optional[datetime] = SQLModelField(
        default_factory=datetime.now,
        nullable=False,
        description="The timestamp when the record was created"
    )
    updated_at: Optional[datetime] = SQLModelField(
        default_factory=datetime.now,
        nullable=False,
        description="The timestamp when the record was last updated"
    )


class Paper(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    binded: User
    answer_map: dict
    problems: List[Problem]

    def model_validate_to_end(self):
        for p in self.problems:
            for c in p.candidates:
                c.text = Text.model_validate(c.text)
        
        return self
    
    def with_test_version(self):
        q_a_list = []
        for p in self.problems:
            q = p.question
            a = p.answer
            c = p.wrong

            answers = [a] + c
            random.shuffle(answers)
            q_a_list.append(QA(question=q, answers=answers))

        return TestPaper(
            id=self.id, 
            binded=self.binded,
            q_a_set=q_a_list
        )

    def score(self):
        all_weights = 0
        weight_map = {}

        for p in self.problems:
            match p.difficulty:
                case Difficulty.EASY:
                    weight = 1
                case Difficulty.MODERATE:
                    weight = 2
                case Difficulty.HARD:
                    weight = 3
                case _:
                    weight = 2
            
            weight_map[p.id] = [weight, p.corrected]
            
            all_weights += weight

        normalized_score_map = {
            id: [(weight[0] / all_weights) * 100, weight[1]] for id, weight in weight_map.items()
        }

        sum = 0
        for _, score in normalized_score_map.items():
            if score[1]:
                sum += score[0]

        return sum
            

    def get_p_counts(self) -> int:
        """ 하나의 시험용지에 속한 문제들의 개수: int 를 리턴합니다 """
        return len(self.problems)
    
    def get_owner_id(self) -> uuid.UUID:
        """ 하나의 시험용지에 바인딩된 유저의 id: uuid.UUID 를 리턴합니다. """
        return self.binded.id
    
    def get_owner_name(self) -> str:
        """ 하나의 시험용지에 바인딩된 유저의 이름: str 을 리턴합니다."""
        return self.binded.name
    

class TestPaper(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    binded: User
    q_a_set: List[QA]

    def to_published_version(self, paper: Paper) -> Paper:
        checked_map = {}
        
        for qa in self.q_a_set:
            for a in qa.answers:
                if a.checked:
                    checked_map[qa.question.u_id] = a.u_id
                    break

        for p in paper.problems:
            checked_candidate_id = checked_map.get(p.u_id)
            
            if checked_candidate_id is not None:
                p.set_checked(checked_candidate_id)
                
        return paper
                    
if __name__ == "__main__":
    from app.core.db import engine
    SQLModel.metadata.create_all(engine)