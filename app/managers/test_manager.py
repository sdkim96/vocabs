from app.schemas.auth import User
from app.schemas.problem import TestPaper
from app.factory.problem import ProblemFactory

class TestManager:
    
    def __init__(
        self,
        problem_factory: ProblemFactory = ProblemFactory(),
        user: User = User()
    ) -> None:
        
        self.problem_factory = problem_factory
        self.user = user
        
    def publish(self) -> TestPaper:
        imported = self.problem_factory.run_pipeline()
        if imported is None:
            raise ValueError("problem을 생성하는데 문제가 발생함")
        self.imported = imported
        
        return TestPaper(binded = self.user, problems=self.imported.problems)

    
    def evaluate(self, test_paper: TestPaper):
        
        return test_paper.score()
    
    