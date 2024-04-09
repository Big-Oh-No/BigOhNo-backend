from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, asc
from ..utils.db import get_db
from ..utils.utils import hash
from ..models import user_model, course_model, disscussion_model
from ..schemas import user_schema, discussion_schema
from typing import List, Optional
import re
from datetime import datetime

router = APIRouter(
    prefix="/discussion",
    tags=["discussion"],
)



@router.post(
    "/{course_id}",
    status_code=200,
    response_model=List[discussion_schema.Discussion]
)
async def get_discussions(
    course_id: int,
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),
):
    """Gets all the discussions in a course"""

    user_profile = db.query(user_model.User).filter(and_(user_model.User.email == user.email, user_model.User.password == hash(user.password))).first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    if not user_profile.verified:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unverified User"
        )
    
    course = db.query(course_model.Course).filter(course_model.Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such course exists"
        )
    
    if user_profile.role == user_model.RoleEnum.student:
        student = db.query(user_model.Student).filter(user_model.Student.user_id == user_profile.id).first()
        
        if not student:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unexpected error occured"
        )

        enrollment = db.query(course_model.Enrollment).filter(and_(course_model.Enrollment.course_id == course_id, course_model.Enrollment.student_id == student.id)).first()

        if not enrollment:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student is not enrolled in the course"
            )
    
    if user_profile.role == user_model.RoleEnum.teacher:
        teacher = db.query(user_model.Teacher).filter(user_model.Teacher.user_id == user_profile.id).first()
        
        if not teacher:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unexpected error occured"
        )

        if course.teacher_id != teacher.id:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Teacher is not taking the course"
            )
    
    if user_profile.role == user_model.RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin do not have access to discussion board"
            )
    
    discussions = db.query(disscussion_model.Discussion).filter(disscussion_model.Discussion.course_id == course.id).order_by(desc(disscussion_model.Discussion.updated_at)).all()

    result = []
    for discussion in discussions:
        author = db.query(disscussion_model.Message).filter(disscussion_model.Message.discussion_id == discussion.id).order_by(asc(disscussion_model.Message.created_at)).first()

        if not author:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unexpected error occured"
            )
        
        author_user = db.query(user_model.User).filter(user_model.User.id == author.user_id).first()

        if not author_user:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unexpected error occured"
            )
        
        num_messages = db.query(disscussion_model.Message).filter(disscussion_model.Message.discussion_id == discussion.id).count()

        result.append(discussion_schema.Discussion(
            id=discussion.id,
            title=discussion.title,
            num_replies=num_messages,
            date_created=discussion.created_at,
            author_name=f'{author_user.first_name} {author_user.last_name}',
            author_pfp=author_user.profile_image
        ))
        
    return result


@router.post(
    "/create/{course_id}",
    status_code=201,
)
async def create_discussion(
    course_id: int,
    user: discussion_schema.CreateDiscussion,
    db: Session = Depends(get_db),
):
    """Creates a discussion thread"""

    user_profile = db.query(user_model.User).filter(and_(user_model.User.email == user.email, user_model.User.password == hash(user.password))).first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    course = db.query(course_model.Course).filter(course_model.Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such course exists"
        )
    
    if user_profile.role == user_model.RoleEnum.student:
        student = db.query(user_model.Student).filter(user_model.Student.user_id == user_profile.id).first()
        
        if not student:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unexpected error occured"
        )

        enrollment = db.query(course_model.Enrollment).filter(and_(course_model.Enrollment.course_id == course_id, course_model.Enrollment.student_id == student.id)).first()

        if not enrollment:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student is not enrolled in the course"
            )
    
    if user_profile.role == user_model.RoleEnum.teacher:
        teacher = db.query(user_model.Teacher).filter(user_model.Teacher.user_id == user_profile.id).first()
        
        if not teacher:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unexpected error occured"
        )

        if course.teacher_id != teacher.id:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Teacher is not taking the course"
            )
    
    if user_profile.role == user_model.RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin do not have access to discussion board"
            )
    
    discussion = disscussion_model.Discussion(
        title=user.title,
        course_id=course_id
    )

    db.add(discussion)
    db.commit()
    db.refresh(discussion)

    message = disscussion_model.Message(
        content=user.content,
        discussion_id=discussion.id,
        user_id=user_profile.id
    )

    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {"message": "discussion created successfully"}

@router.post(
    "/message/{discussion_id}",
    response_model=List[discussion_schema.DiscussionThreadMessage],
    status_code=200,
)
async def get_thread(
    discussion_id: int,
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),
):
    """gets one single discussion thread"""

    user_profile = db.query(user_model.User).filter(and_(user_model.User.email == user.email, user_model.User.password == hash(user.password))).first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    discussion = db.query(disscussion_model.Discussion).filter(disscussion_model.Discussion.id == discussion_id).first()
    
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such discussion exists"
        )
    
    course_id = discussion.course_id
    
    course = db.query(course_model.Course).filter(course_model.Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such course exists"
        )
    
    if user_profile.role == user_model.RoleEnum.student:
        student = db.query(user_model.Student).filter(user_model.Student.user_id == user_profile.id).first()
        
        if not student:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unexpected error occured"
        )

        enrollment = db.query(course_model.Enrollment).filter(and_(course_model.Enrollment.course_id == course_id, course_model.Enrollment.student_id == student.id)).first()

        if not enrollment:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student is not enrolled in the course"
            )
    
    if user_profile.role == user_model.RoleEnum.teacher:
        teacher = db.query(user_model.Teacher).filter(user_model.Teacher.user_id == user_profile.id).first()
        
        if not teacher:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unexpected error occured"
        )

        if course.teacher_id != teacher.id:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Teacher is not taking the course"
            )
    
    if user_profile.role == user_model.RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin do not have access to discussion board"
            )
    
    messages = (
        db
        .query(
            disscussion_model.Message.id,
            disscussion_model.Message.content,
            disscussion_model.Message.upvotes,
            disscussion_model.Message.created_at,
            user_model.User.first_name,
            user_model.User.last_name,
            user_model.User.profile_image    
        )
        .join(user_model.User, disscussion_model.Message.user_id == user_model.User.id)
        .filter(disscussion_model.Message.discussion_id == discussion_id)
        .order_by(asc(disscussion_model.Message.created_at))
        .all()
    )

    result = []

    for message in messages:
        result.append(
            discussion_schema.DiscussionThreadMessage(
                id=message.id,
                message=message.content,
                upvotes=message.upvotes,
                date_created=message.created_at,
                author_name=f'{message.first_name} {message.last_name}',
                author_pfp=message.profile_image
            )
        )
    
    return result

@router.post(
    "/send/{discussion_id}",
    status_code=201,
)
async def send_message(
    discussion_id: int,
    user: discussion_schema.CreateMessage,
    db: Session = Depends(get_db),
):
    """Sends a message in discussion thread"""

    user_profile = db.query(user_model.User).filter(and_(user_model.User.email == user.email, user_model.User.password == hash(user.password))).first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    discussion = db.query(disscussion_model.Discussion).filter(disscussion_model.Discussion.id == discussion_id).first()
    
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such discussion exists"
        )
    
    course_id = discussion.course_id
    
    course = db.query(course_model.Course).filter(course_model.Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such course exists"
        )
    
    if user_profile.role == user_model.RoleEnum.student:
        student = db.query(user_model.Student).filter(user_model.Student.user_id == user_profile.id).first()
        
        if not student:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unexpected error occured"
        )

        enrollment = db.query(course_model.Enrollment).filter(and_(course_model.Enrollment.course_id == course_id, course_model.Enrollment.student_id == student.id)).first()

        if not enrollment:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student is not enrolled in the course"
            )
    
    if user_profile.role == user_model.RoleEnum.teacher:
        teacher = db.query(user_model.Teacher).filter(user_model.Teacher.user_id == user_profile.id).first()
        
        if not teacher:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unexpected error occured"
        )

        if course.teacher_id != teacher.id:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Teacher is not taking the course"
            )
    
    if user_profile.role == user_model.RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin do not have access to discussion board"
            )
    
    message = disscussion_model.Message(
        content=user.content,
        discussion_id=discussion.id,
        user_id=user_profile.id
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    discussion.updated_at = datetime.now()
    db.commit()
    db.refresh(discussion)
    
    return {"message": "message sent successfully"}