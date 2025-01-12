import uuid

from pydantic import BaseModel, Field
from sqlmodel import SQLModel
from app.schemas.enum import UType

class Token(BaseModel):
    token: str

class UserDTO(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = "admin"

class User(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = "admin"
    password: str = "aaaa"
    user_type: UType = UType.ADMIN

