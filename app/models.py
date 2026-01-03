from typing import List, Optional
from enum import Enum
from datetime import date, time
from sqlmodel import SQLModel, Field, Relationship
from .date_time import ist_date, ist_time


class Frequency(str, Enum):
    daily = "daily"
    weekly = "weekly"

class Status(str, Enum):
    completed = "completed"
    missed = "missed"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    habits: List["Habit"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete"})

class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    frequency: Frequency = Field(default=Frequency.daily)
    created_at: date = Field(default_factory=ist_date)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="habits")
    logs: List["HabitLog"] = Relationship(
        back_populates="habit",
        sa_relationship_kwargs={"cascade": "all, delete"})

class HabitLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    logDate: date = Field(default_factory=ist_date)
    logTime: time = Field(default_factory=ist_time)
    status: Status = Field(default=Status.missed)
    habit_id: int = Field(foreign_key="habit.id")
    habit: Optional[Habit] = Relationship(back_populates="logs")