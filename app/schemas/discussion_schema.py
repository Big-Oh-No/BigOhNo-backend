from datetime import date, datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from ..models import user_model, course_model


class Discussion(BaseModel):
    id: int
    title: str
    num_replies: int
    date_created: datetime
    author_name: str
    author_pfp: Optional[str]

    class Config:
        from_attributes = True


class CreateDiscussion(BaseModel):
    email: str
    password: str

    # discussion related
    title: str

    # message related
    content: str

    class Config:
        from_attributes = True

class CreateMessage(BaseModel):
    email: str
    password: str

    # discussion related
    content: str

    class Config:
        from_attributes = True

class DiscussionThreadMessage(BaseModel):
    id: int
    message: str
    upvotes: int
    date_created: datetime
    author_name: str
    author_pfp: Optional[str]

    class Config:
        from_attributes = True
