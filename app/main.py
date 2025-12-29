from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import users, habits

app = FastAPI()

@app.on_event("startup")
def startup_event():
    create_db_and_tables()

app.include_router(users.router)
app.include_router(habits.router)