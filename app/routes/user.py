from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from ..utils.db import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post(
    "/login",
    status_code=200
)
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db),    
):
    """Logs a user in"""
    print(f"email {email}")
    print(f"password {password}")
