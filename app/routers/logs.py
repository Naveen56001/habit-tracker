from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
from sqlmodel import select
from ..database import get_session
from ..models import HabitLog, Habit
from ..schemas import LogCreate, LogRead, LogUpdate
from sqlmodel import Session


router = APIRouter(prefix="/log", tags=["logs"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=List[LogRead])
def get_log(session: SessionDep, offset: int = 0, limit: int = 10):
    logs = session.exec(select(HabitLog).offset(offset).limit(limit)).all()
    return logs

@router.post("/", response_model=LogRead)
def post_log(session: SessionDep, payload: LogCreate):
    habit = session.get(Habit, payload.habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail=f"Habit with id {payload.habit_id} does not exist")
    log = HabitLog.model_validate(payload)
    session.add(log)
    session.commit()
    session.refresh(log)

    return log

@router.get("/{id}", response_model=LogRead)
def get_one_log(id: int, session: SessionDep):
    log = session.get(HabitLog, id)
    if not log:
        raise HTTPException(status_code=404, detail=f"Habit log with id {id} does not exist")
    return log

@router.put("/{id}")
def update_log(session: SessionDep, id: int, update: LogUpdate):
    log = session.get(HabitLog, id)
    if not log:
        raise HTTPException(status_code=404, detail="Habit log not found.")
    if update.status is not None:
        log.status = update.status
    
    session.add(log)
    session.commit()
    session.refresh(log)
    
    return {"message": "Updation successfull"}

@router.delete("/{id}")
def delete_log(session: SessionDep, id: int):
    log = session.get(HabitLog, id)
    if not log:
        raise HTTPException(status_code=404, detail="Habit log not found.")
    session.delete(log)
    session.commit()

    return {"ok": True}