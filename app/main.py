from fastapi import Depends, FastAPI
from .utils.db import get_db
from sqlalchemy.orm import Session
# from .routes import 
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(*.router)  

@app.get("/")
async def root():
    return {"message": "Korse Backend v0.0.1"}