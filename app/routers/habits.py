from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
from sqlmodel import select
from ..database import get_session
from ..models import Habit, User
from ..schemas import HabitCreate, HabitRead, UpdateHabit
from sqlmodel import Session

router = APIRouter(prefix="/habit", tags=["habits"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/", response_model=HabitRead)
def create_habit(payload: HabitCreate, session: SessionDep):
    user = session.get(User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"There is no user with id {payload.user_id}")
    
    habit = Habit.model_validate(payload)
    session.add(habit) 
    session.commit() 
    session.refresh(habit)

    return habit

@router.get("/", response_model=List[HabitRead])
def list_habits(session: SessionDep, offset: int = 0, limit: int = 10):
    habits = session.exec(select(Habit).offset(offset).limit(limit)).all()
    return habits

@router.get("/{id}", response_model=HabitRead)
def get_one_habit(id: int, session: SessionDep):
    habit = session.get(Habit, id)
    if not habit:
        raise HTTPException(status_code=404, detail=f"No habit with id {id}")
    return habit

@router.put("/{id}")
def update_habit(id: int, update: UpdateHabit, session: SessionDep):
    habit = session.get(Habit, id)
    if not habit: 
        raise HTTPException(404, "not found")
    if update.title is not None: 
        habit.title = update.title
    if update.description is not None: 
        habit.description = update.description
    if update.frequency is not None:
        habit.frequency = update.frequency

    session.add(habit)
    session.commit()
    session.refresh(habit)
    return {"message": "Updation Successful"}

@router.delete("/{id}")
def delete_habit(id: int, session: SessionDep):
    habit = session.get(Habit, id)
    if not habit: 
        raise HTTPException(404, "not found") 
    session.delete(habit)
    session.commit()
    return {"ok": True}