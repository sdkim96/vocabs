import uuid
from typing import List

from sqlmodel import Session, select
from app.schemas import (
    Paper, 
    UserDTO, 
    User, 
    PaperStore,
    StoreSearchOption,
    PaperMeta
)
from app.factory.problem import ProblemFactory

class Publisher:
    
    def __init__(
        self,
        request_key: uuid.UUID = uuid.uuid4(),
        target_user: UserDTO = UserDTO()
        
    ) -> None:
        
        self.request_key = request_key
        self.target_user = target_user

    def publish_paper(self, problem_factory: ProblemFactory) -> Paper:
        imported = problem_factory.run_pipeline()
        if imported is None:
            raise ValueError("problem을 생성하는데 문제가 발생함")
        self.imported = imported
        
        return Paper(
            binded = self.target_user, 
            answer_map=imported.answer_map, 
            problems=self.imported.problems
        )
    
    def get_papers_by_user(self, db: Session, user: User, option: StoreSearchOption = StoreSearchOption.ALL) -> List[Paper] | List[PaperStore] | List[PaperMeta]:
        """ 같은 학생이 푼 서로다른 문제지들을 가져옴 """

        namespace = (user.id,)
        papers = PaperStore.search(db, namespace, option) # type: ignore
        
        return papers

    def get_papers_by_paper(self, db: Session, paper: Paper) -> List[Paper]:
        """ 같은 문제지들을 가져옴"""
        
        with db as session:
            stmt = (
                select(PaperStore.value)
                .where(PaperStore.key == str(paper.id))
            )
            papers = session.exec(stmt).fetchall()
        
        same_papers = []
        for paper in papers: # type: ignore
            casted = Paper.model_validate(paper)
            casted.model_validate_to_end()

            same_papers.append(casted)

        return same_papers