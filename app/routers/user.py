from typing import Annotated
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import (
    UserDTO,
    UserCreate, 
    User,
    Token,
    UType,
    GetStudentsResponse
)
from app.deps import (
    Session, 
    get_db, 
    get_current_user
)

user_r = APIRouter()

@user_r.post("/sign_up", response_model=UserDTO)
async def sign_up(new_user: UserCreate, db: Session = Depends(get_db)):
    
    created = User.create(db, user=new_user)
    if created:
        return UserDTO(
            id=created.id, 
            name=created.name, 
            user_type=created.user_type,
            user_name=created.user_name,
            user_nickname=created.user_nickname,
        )
    
    raise HTTPException(status_code=500, detail="User already exists")

@user_r.post("/sign_in", response_model=Token)
async def sign_in(user: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    
    me = User.get(db, user.username)

    if not me:
        raise HTTPException(status_code=500, detail="User not found")
    
    if me.verify(user.password):
        token = Token.new(me)
        return token
    else:
        raise HTTPException(status_code=500, detail="Password not matched")


@user_r.get("/me", response_model=UserDTO)
async def get_me(me: User = Depends(get_current_user)):
    return UserDTO(
        id=me.id, 
        name=me.name, 
        user_type=me.user_type,
        user_name=me.user_name,
        user_nickname=me.user_nickname,
    )


@user_r.get("/students", response_model=GetStudentsResponse)
async def get_students(me: User = Depends(get_current_user), db: Session = Depends(get_db)):
        
    if me.user_type not in [UType.TEACHER, UType.ADMIN]:
        raise HTTPException(status_code=403, detail="You are not a teacher")
    
    all_user = User.get_all(db)
    if not all_user:
        raise HTTPException(status_code=404, detail="No student found")
    
    return GetStudentsResponse(
        students=[
            UserDTO(
                id=each.id, 
                name=each.name,
                user_name=each.user_name,
                user_nickname=each.user_nickname,
            ) 
            for each in all_user if each.user_type == UType.STUDENT
        ]
    )
