import uuid
from typing import Optional
from app.schemas.auth import UserDTO
from app.schemas import Paper
from app.factory.problem import ProblemFactory

class TestManager:
    
    def __init__(
        self,
        request_key: uuid.UUID = uuid.uuid4(),
        user: UserDTO = UserDTO()

    ) -> None:
        
        self.request_key = request_key
        self.user = user

    def publish_paper(self, problem_factory: ProblemFactory) -> Paper:
        imported = problem_factory.run_pipeline()
        if imported is None:
            raise ValueError("problem을 생성하는데 문제가 발생함")
        self.imported = imported
        
        return Paper(
            binded = self.user, 
            answer_map=imported.answer_map, 
            problems=self.imported.problems
        )
    
    def calculate_test_time(self):
        pass