from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..utils.db import get_db
from ..utils.utils import hash
from ..models import user_model
from ..schemas import user_schema

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post(
    "/login",
    status_code=200,
)
async def login(
    user: user_schema.User,
    db: Session = Depends(get_db),    
):
    """Logs a user in"""
    
    user = db.query(user_model.User).filter(and_(user_model.User.email == user.email,user_model.User.password == hash(user.password))).first()

    if not user:
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    return {"message" : "User Authenticated"}