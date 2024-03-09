from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..utils.db import get_db
from ..utils.utils import hash
from ..models import user as user_model

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post(
    "/login",
    status_code=200
)
async def login(
    request: Request,
    db: Session = Depends(get_db),    
):
    """Logs a user in"""
    data = await request.json()
    email = data["email"]
    password = data["password"]
    
    user = db.query(user_model.User).filter(and_(user_model.User.email == email,user_model.User.password == hash(password))).first()

    if not user:
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong password and username combination"
        )
    
    return {"message" : "User Authenticated"}