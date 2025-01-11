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

class Question(BaseModel):
    u_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    content: str

class Answer(BaseModel):
    u_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    content: str
    checked: bool = False

class QA(BaseModel):
    question: Question
    answers: List[Answer] 

class Text(SQLModel, table=True):
    id: int = sqlmodelField(primary_key=True)
    name: str
    tag: Tag = sqlmodelField(default=Tag.UNDECIDED)
    k_description: str
        

class Candidate(BaseModel):
    id: int = 0
    u_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    text: Text
    answer: bool = False
    checked: bool = False


class Problem(BaseModel):
    """
    problem.question: Question()
        - question.u_id는 problem.u_id과 같은 값
    problem.answer: Answer()
        - answer.u_id는 candidate.u_id와 같은 값
    """
    id: int
    u_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    difficulty: Difficulty = Field(default=Difficulty.MODERATE)
    question_type: QType = QType.KOREAN
    candidates: List[Candidate]

    @property
    def question(self) -> Question:
        answer_obj = self.get_answer_obj()
        if self.question_type == QType.KOREAN:
            question = answer_obj.text.k_description
        else:
            question = answer_obj.text.name
            
        return Question(u_id=self.u_id, content=question)


    @property
    def answer(self) -> Answer:
        answer_obj = self.get_answer_obj()
        if self.question_type == QType.KOREAN:
            answer = answer_obj.text.name
        else:
            answer = answer_obj.text.k_description
            
        return Answer(u_id= answer_obj.u_id, content=answer)
    

    @property
    def wrong(self) -> List[Answer]:
        wrong_objs = self.get_wrong_objs()

        if self.question_type == QType.KOREAN:
            wrongs = [Answer(u_id= obj.u_id, content=obj.text.name) for obj in wrong_objs]
        else:
            wrongs = [Answer(u_id= obj.u_id, content=obj.text.k_description) for obj in wrong_objs]
        
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
    

    def set_checked(self, candidate_id):
        for c in self.candidates:
            if c.u_id == candidate_id:
                c.checked = True
            else:
                c.checked = False
        
        return self

    
if __name__ == "__main__":
    from app.core.db import engine
    SQLModel.metadata.create_all(engine)