from sqlmodel import SQLModel
from typing import Optional

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
    frequency: Optional[str] = "daily"
    user_id: int

class HabitRead(SQLModel):
    id: int
    title: str
    description: str
    frequency: str
    created_at: str
    user_id: int

class UpdateHabit(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None