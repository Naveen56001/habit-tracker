from typing import List, Optional
from enum import Enum
import datetime
from sqlmodel import SQLModel, Field, Relationship

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
    habits: List["Habit"] = Relationship(back_populates="user")

class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    frequency: Frequency = Field(default=Frequency.daily)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="habits")
    logs: List["HabitLog"] = Relationship(back_populates="habit")

class HabitLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    status: Status = Field(default=Status.missed)
    habit_id: int = Field(foreign_key="habit.id")
    habit: Optional[Habit] = Relationship(back_populates="logs")