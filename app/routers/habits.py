from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
from sqlmodel import select
from ..database import get_session
from ..models import Habit
from ..schemas import HabitCreate, HabitRead, UpdateHabit
from sqlmodel import Session

router = APIRouter(prefix="/habit", tags=["habits"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/", response_model=HabitRead)
def create_habit(payload: HabitCreate, session: SessionDep):
    habit = Habit.model_validate(payload)
    session.add(habit) 
    session.commit() 
    session.refresh(habit)

    return habit

@router.get("/", response_model=List[HabitRead])
def list_habits(session: SessionDep, offset: int = 0, limit: int = 10):
    habits = session.exec(select(Habit).offset(offset).limit(limit)).all()
    return habits

@router.put("/{id}")
def update_habit(id: int, update: UpdateHabit, session: SessionDep):
    habit = session.get(Habit, id)
    if not habit: 
        raise HTTPException(404, "not found")
    if update.title: 
        habit.title = update.title
    if update.description: 
        habit.description = update.description
    if update.frequency:
        habit.frequency = update.frequency

    session.add(habit)
    session.commit()
    session.refresh(habit)
    return habit

@router.delete("/{id}")
def delete_habit(id: int, session: SessionDep):
    habit = session.get(Habit, id)
    if not habit: 
        raise HTTPException(404, "not found")
    
    session.delete(habit)
    session.commit()
    return {"ok": True}