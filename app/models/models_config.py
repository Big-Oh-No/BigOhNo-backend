from .user_model import User, Teacher, Admin, Student
from .course_model import Enrollment, Course, Assignment, Submission
from .disscussion_model import Discussion, Message
from ..utils.db import Base

user = User()
admin = Admin()
teacher = Teacher()
student = Student()
course = Course()
enrollment = Enrollment()
assignment = Assignment()
submission = Submission()
discussion = Discussion()
message = Message()