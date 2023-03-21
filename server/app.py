from fastapi import FastAPI
from .routers import ums_signup
from database import SessionLocal, db_engine, Base

Base.metadata.create_all(bind=db_engine)

app = FastAPI()
app.include_router(ums_signup.router)
