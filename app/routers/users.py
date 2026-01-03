from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
from sqlmodel import select
from ..database import get_session
from ..models import User
from ..schemas import UserCreate, UserRead, UpdateUser
from sqlmodel import Session

router = APIRouter(prefix="/user", tags=["users"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/", response_model=UserRead)
def create_user(payload: UserCreate, session: SessionDep):
    user = User.model_validate(payload)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/", response_model=List[UserRead])
def list_users(session: SessionDep, offset: int = 0, limit: int = 10):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@router.get("/{id}", response_model=UserRead)
def get_user(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{id}")
def update_user(id: int, update: UpdateUser, session: SessionDep):
    user = session.get(User, id)
    if not user: 
        raise HTTPException(404, "not found")
    if update.name is not None: 
        user.name = update.name
    if update.email is not None: 
        user.email = update.email

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "Updation Successfull"}

@router.delete("/{id}")
def delete_user(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user: 
        raise HTTPException(404, "not found") 
    session.delete(user)
    session.commit()
    return {"ok": True}