import uuid
import re
from typing import (
    List, 
    Optional
)
from sqlmodel import SQLModel, Field as sqlmodelField
from pydantic import BaseModel, field_validator, Field

from app.schemas.enum import Tag, Difficulty, QType
from app.schemas.auth import User


class Text(SQLModel, table=True):
    id: int | None = sqlmodelField(default=None, primary_key=True)
    name: str
    tag: Tag = sqlmodelField(default=Tag.UNDECIDED)
    k_description: str
        

class Candidate(BaseModel):
    id: int = 0
    text: Text
    answer: bool = False
    checked: bool = False


class Problem(BaseModel):
    id: int
    difficulty: Difficulty = Field(default=Difficulty.MODERATE)
    question_type: QType = QType.KOREAN
    candidates: List[Candidate]

    @property
    def question(self) -> str:
        answer = self.get_answer_obj()
        if self.question_type == QType.KOREAN:
            question = answer.text.k_description
        else:
            question = answer.text.name
            
        return question
    
    @property
    def answer(self) -> str:
        answer_obj = self.get_answer_obj()
        if self.question_type == QType.KOREAN:
            answer = answer_obj.text.name
        else:
            answer = answer_obj.text.k_description
            
        return answer
    
    @property
    def wrong(self) -> List[str]:
        wrong_objs = self.get_wrong_objs()

        if self.question_type == QType.KOREAN:
            wrongs = [obj.text.name for obj in wrong_objs]
        else:
            wrongs = [obj.text.k_description for obj in wrong_objs]
        
        return wrongs
        
    
    @property
    def len_of_options(self) -> int:
        return len(self.candidates)

    @property
    def corrected(self) -> bool:
        answer_obj = self.get_answer_obj()
        return answer_obj.checked
    
    def validate(self):
        """
        1. 하나의 문제에 정답 하나
        2. 하나의 문제에 중복된 candidate 없기
        """
        seen = set()

        # 중복된 candidate 없어야함
        for c in self.candidates:
            if c.id in seen:
                raise ValueError("하나의 문제에 중복된 candidate가 있습니다.") 
            else:
                seen.add(c.id)
        
        true_answers = [candidate for candidate in self.candidates if candidate.answer]
        
        # 검증: True인 항목이 반드시 하나여야 함
        if len(true_answers) != 1:
            raise ValueError("하나의 문제는 answer=True이어야 합니다.")
        
        # 검증: Candidates는 연속적이어야 합니다.
        ids = sorted([c.id for c in self.candidates])
        if ids != list(range(min(ids), max(ids) + 1)):
            raise ValueError("Candidates의 ID는 연속적이어야 합니다.")

    def get_answer_obj(self) -> Candidate:
        
        for c in self.candidates:
            if c.answer is True:
                return c
        
        raise ValueError("정답이 없습니다.")
    
    def get_wrong_objs(self) -> List[Candidate]:
        
        wrongs = []
        for c in self.candidates:
            if c.answer is False:
                wrongs.append(c)
        
        return wrongs
    
        
            

class TestPaper(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    binded: User
    problems: List[Problem]
    
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
            
            weight_map[p.id] = weight
            all_weights += weight

        normalized_score_map = {
            id: (weight / all_weights) * 100 for id, weight in weight_map.items()
        }

        total_score = sum(normalized_score_map.values())
        
        return total_score
                


    def get_p_counts(self) -> int:
        """ 하나의 시험용지에 속한 문제들의 개수: int 를 리턴합니다 """
        return len(self.problems)
    
    def get_owner_id(self) -> uuid.UUID:
        """ 하나의 시험용지에 바인딩된 유저의 id: uuid.UUID 를 리턴합니다. """
        return self.binded.id
    
    def get_owner_name(self) -> str:
        """ 하나의 시험용지에 바인딩된 유저의 이름: str 을 리턴합니다."""
        return self.binded.name
    
if __name__ == "__main__":
    from app.core.db import engine
    SQLModel.metadata.create_all(engine)