import random
import uuid
from datetime import datetime
from typing import (
    List, 
    Optional, 
    Dict, 
    Tuple,
    Any
)
from pydantic import BaseModel, Field

from sqlmodel import SQLModel, Session, select, Field as SQLModelField
from sqlalchemy.dialects.postgresql import JSONB

from app.schemas.enum import Difficulty
from app.schemas.problem import Problem, QA, Text
from app.schemas.auth import User, UserDTO


class PaperStore(SQLModel, table=True):
    """
    prefix: 유저id, 문제지의 id의 조합
    key: request_id (문제를 요청할때의 request_id)
    value: 문제지의 정보를 담고 있는 dict

    
    """

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

    @classmethod
    def search(
        cls,
        db: Session,
        namespace: Tuple[Any, ...]
    ) -> List["PaperStore"]:
        """ """
        try:
            prefix_pattern = "%"+ ".".join(map(str, namespace)) + "%"
            stmt = (
                select(cls)
                .where(cls.prefix.like(prefix_pattern)) # type: ignore
            )
            return db.exec(stmt).all() # type: ignore
            
        except Exception as e:
            raise e
    

    @classmethod
    def get(
        cls,
        db: Session,
        namespace: Tuple[Any, ...],
        key: Any
    ) -> Optional[Dict]:
        """ """
        try:
            prefix = ".".join(map(str, namespace))
            stmt = (
                select(cls.value)
                .where(cls.prefix == prefix)
                .where(cls.key == str(key))
            )
            return db.exec(stmt).first() # type: ignore
        except Exception as e:
            raise e
    

    @classmethod
    def put(
        cls,
        db: Session,
        namespace: Tuple[Any, ...],
        key: Any,
        value: Dict
    ) -> None:
        """ """
        try:
            prefix = ".".join(map(str, namespace))
            
            # 기존 레코드 조회
            statement = select(cls).where(cls.prefix == prefix, cls.key == str(key))
            result = db.exec(statement).first()
            
            if result:
                result.value = value
                result.updated_at = datetime.now()
                db.add(result)
            else:
                new_record = cls(
                    prefix=prefix,
                    key=str(key),
                    value=value,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.add(new_record)
            
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

class Paper(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    binded: UserDTO
    answer_map: dict
    problems: List[Problem]

    def model_validate_to_end(self):
        for p in self.problems:
            for c in p.candidates:
                c.text = Text.model_validate(c.text)
        
        return self
    
    def to_test_version(self, test_id: uuid.UUID):
        q_a_list = []
        
        for p in self.problems:
            q = p.question
            a = p.answer
            c = p.wrong

            answers = [a] + c
            random.shuffle(answers)
            q_a_list.append(QA(question=q, answers=answers))

        return TestPaper(
            paper_id=self.id, 
            test_id=test_id,
            binded=self.binded,
            q_a_set=q_a_list
        )

    def calculate_score(self):
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
    paper_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    test_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    binded: UserDTO
    q_a_set: List[QA]

    def apply_changes(self, paper: Paper) -> Paper:
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