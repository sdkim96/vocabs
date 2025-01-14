import datetime
import jwt
import uuid
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Session, Field as SQLModelField, select

from argon2 import PasswordHasher

from app.schemas.enum import UType
from app.core.config import settings
from app.core.db import engine

encoder = PasswordHasher()


class UserCreate(BaseModel):
    name: str
    password: str

    user_name: str = "김성동"
    user_nickname: str = "김성동"

class UserDTO(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = "admin"

    user_name: str = "김성동"
    user_nickname: str = "김성동"
    user_type: UType = UType.STUDENT

class User(SQLModel, table=True):

    __table_args__ = {"extend_existing": True}

    id: uuid.UUID = SQLModelField(default_factory=uuid.uuid4, primary_key=True)  # 기본 키로 설정
    name: str = SQLModelField(default="admin")
    password: str = SQLModelField(default="aaaa")
    
    user_name: str = SQLModelField(default="김성동")
    user_nickname: str = SQLModelField(default="김성동")
    user_type: UType = SQLModelField(default=UType.GUEST)

    @classmethod
    def get_all(cls, db: Session):
        try:
            stmt = select(cls)
            return db.exec(stmt).all()
        except Exception as e:
            print("유저 정보 조회중 오류남: ", e)
            return None

    @classmethod
    def create(cls, db: Session, user: UserCreate):
        
        try:
            exist = cls.get(db, user.name)
            if exist:
                return None
        except Exception as e:
            print("유저 중복 확인중 오류남: ", e)
            return None
        
        hashed = encoder.hash(user.password+settings.PEPPER)

        try:
            new_record = cls(
                id=uuid.uuid4(),
                name=user.name,
                password=hashed,
                user_name=user.user_name,
                user_nickname=user.user_nickname,
                user_type=UType.STUDENT
            )
            db.add(new_record)
            db.commit()
            return new_record
        except Exception as e:
            db.rollback()
            print("유저 생성중 오류남: ", e)
            return None
        
    @classmethod
    def get(cls, db: Session, name: str):
        try:
            stmt = select(cls).where(cls.name == name)
            return db.exec(stmt).first()
        except Exception as e:
            print("유저 정보 조회중 오류남: ", e)
            return None
        
    @classmethod
    def get_by_id(cls, db: Session, id: uuid.UUID):
        try:
            stmt = select(cls).where(cls.id == id)
            return db.exec(stmt).first()
        except Exception as e:
            print("유저 정보 조회중 오류남: ", e)
            return
        

    def verify(self, password: str):
        try:
            return encoder.verify(self.password, password+settings.PEPPER)
        except Exception:
            return False

class Payload(BaseModel):
    sub: str
    exp: datetime.datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    @classmethod
    def new(cls, user: User):
        expiration = datetime.datetime.now() + datetime.timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
        # 페이로드 생성
        payload = {
            "sub": str(user.name),  # 사용자 ID
            "exp": expiration,  # 만료 시간
        }
        
        # JWT 생성
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        
        return cls(access_token=token)
    

if __name__ =="__main__":
    SQLModel.metadata.create_all(engine)