import uuid
import collections
import random
from sqlmodel import select, Session
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.problem import Candidate, Problem, Text

class Exportation(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    answer_map: dict
    problems: List[Problem]


class ProblemFactory:

    def __init__(
        self, 
        db_session: Session,
        texts: Optional[List[Text]] = None,
        candidate_limit: int = 4, 
        problems_count: int = 20,
        
        
    ) -> None:
        """ 차후에 옵션값을 줘서 문제 생성시 옵션값을 줄 수 있도록 수정할 예정입니다. """
        self.candidate_limit = candidate_limit
        self.problems_count = problems_count
        if not db_session:
            raise ValueError('db_session이 필요합니다.')
        
        self.db_session = db_session
        
        all_texts = texts if texts else self._load_texts()
        if len(all_texts) < problems_count * candidate_limit:
            raise ValueError('문제 수가 부족합니다.')

        self.choised_texts = self._choice_texts(all_texts, k=(self.problems_count * self.candidate_limit))

        answer_map = {}
        for i in range(self.problems_count):
            answer_map[i] = random.choice(range(self.candidate_limit))

        self.answer_map = answer_map
        

    def run_pipeline(
        self,
        
    ):
        problems = self.create()
        problems =  self.inject_answer(problems)
        problems = self.prepare(problems)
        if problems:
            return self.export(problems)


    def _load_texts(self) -> List[Text]:
        
        stmt = select(Text)
        with self.db_session as s:
            texts = list(s.exec(stmt).fetchall())
        
        return texts

    def _choice_texts(self, texts: List[Text], k: int) -> List[Text]:
        
        choised = random.choices(texts, k=k)
        print(f"총 **{k}**개 만큼의 랜덤한 영단어목록이 **{len(texts)}** 에서 추출되었습니다.")
        
        return choised

    def create(self)-> List[Problem]:
        """ 
        생성자의 promblems_count만큼의 문제를 생성합니다. 
        이 단계에서는 단순히 문제를 '생성' 하는 단계이지, 절대 '준비' 하는 단계는 아님.
        """

        choised = self.choised_texts
        random.shuffle(choised)

        it = iter(choised)
        
        problems= []
        for current_problem_id in range(self.problems_count):

            candidates = []
            for i in range(self.candidate_limit):
                candidate = Candidate(id=i, text=next(it))
                candidates.append(candidate)
            
            problems.append(Problem(id=current_problem_id, candidates=candidates))
            

        print("문제가 생성 되었습니다 > 생성 단계 완료")
        return problems
    

    def inject_answer(self, problems: List[Problem]):

        answer_map = self.answer_map
        for i, problem in enumerate(problems):
            answer_candidate_id = answer_map[i]
            problem.candidates[answer_candidate_id].answer = True

        print("문제에 답주입을 완료했습니다 > 답 주입단계 완료")
        return problems

    def prepare(self, unprepared: List[Problem]):
        

        print("answer map과 candidates들을 실제 candidate의 u_id로 재매핑합니다.")
        new_map = {}
        for problem in unprepared:
            answer = problem.get_answer_obj()
            new_map[problem.u_id] = answer.u_id
        
        self.answer_map = new_map
        
        try:
            for problem in unprepared:
                problem.validate()
        except ValueError:
            return None
        
        print("문제검증을 완료했습니다 > 문제 검증 완료")
        prepared = unprepared
        return prepared
    
    def export(self, prepared):
        
        return Exportation(   
            answer_map=self.answer_map,
            problems=prepared
        )