from fastapi import FastAPI

from app.factory.problem import ProblemFactory
from app.managers.test_manager import TestManager
from app.schemas.problem import TestPaper

app = FastAPI()

problem_factory = ProblemFactory()

@app.get("/api/paper")
async def get_paper():
    manager = TestManager(problem_factory)
    paper = manager.publish()

    return paper


@app.post("/api/submit")
async def submit_paper(paper: TestPaper):
    manager = TestManager(problem_factory)
    score = manager.evaluate(paper)
    return score