from typing import Optional
from pydantic import BaseModel
from ..models import user_model

class UserSignIn(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class UserSignUp(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    password: str
    role: user_model.RoleEnum

    class Config:
        from_attributes = True
