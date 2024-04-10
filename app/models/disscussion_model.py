from ..utils.db import Base
from .user_model import  User
from .course_model import Course
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Discussion(Base):
    __tablename__ = "discussion"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)

    course = relationship("Course", back_populates="discussion")


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    content = Column(String, nullable=False)
    upvotes = Column(Integer, server_default="0", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    discussion_id = Column(Integer, ForeignKey('discussion.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    discussion = relationship("Discussion", back_populates="message")
    user = relationship("User", back_populates="message")

Course.discussion = relationship("Discussion", back_populates="course")

Discussion.message = relationship("Message", back_populates="discussion")
User.message = relationship("Message", back_populates="user")