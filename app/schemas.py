from sqlmodel import SQLModel
from typing import Optional
from .models import Frequency, Status
from datetime import date, time
from pydantic import computed_field

class UserCreate(SQLModel):
    name: str
    email: str

class UserRead(SQLModel):
    id: int
    name: str
    email: str

class UpdateUser(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None

class HabitCreate(SQLModel):
    title: str
    description: str
    frequency: Frequency = Frequency.daily
    user_id: int

class HabitRead(SQLModel):
    id: int
    title: str
    description: str
    frequency: str
    created_at: date
    user_id: int

    @computed_field
    @property
    def formatted_date(self) -> str:
        return self.created_at.strftime("%d-%m-%Y")

class UpdateHabit(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Frequency | None = None

class LogCreate(SQLModel):
    status: Status = Status.missed
    habit_id: int

class LogRead(SQLModel):
    id: int
    status: str
    logDate: date
    logTime: time
    habit_id: int

    @computed_field
    @property
    def formatted_date(self) -> str:
        return self.logDate.strftime("%d-%m-%Y")
    
    @computed_field
    @property
    def formatted_time(self) -> str:
        return self.logTime.strftime("%H:%M")

class LogUpdate(SQLModel):
    status: Status | None = None
    logTime: time | None = None
