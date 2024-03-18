from fastapi import Depends, FastAPI
from .utils.db import get_db
from sqlalchemy.orm import Session
from .routes import user, course
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.config import settings
from .utils.utils import populatedb

app = FastAPI()
logging.basicConfig(level=logging.INFO)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)  
app.include_router(course.router)  

@app.get("/", status_code=200)
async def root(db: Session = Depends(get_db)):
    # comment it on production
    populatedb(db) 
    return {"message": "Korse Backend v0.0.1"}