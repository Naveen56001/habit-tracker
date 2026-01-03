from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import users, habits, logs

app = FastAPI()

@app.on_event("startup")
def startup_event():
    create_db_and_tables()

app.include_router(users.router)
app.include_router(habits.router)
app.include_router(logs.router)