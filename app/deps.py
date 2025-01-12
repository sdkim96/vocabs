import jwt
from collections.abc import Generator
from typing import Annotated

from sqlmodel import Session
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.core.db import engine
from app.core.config import settings
from app.schemas import Payload, User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"api/sign_in"
)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

security = HTTPBearer()

TokenDep = Annotated[str, Depends(reusable_oauth2)]
SessionDep = Annotated[Session, Depends(get_db)]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        payload = Payload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = User.get(db = session, name=payload.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
