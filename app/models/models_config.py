from .user_model import User, Teacher, Admin, Student
from .course_model import Enrollment, Course
from ..utils.db import Base

user = User()
admin = Admin()
teacher = Teacher()
student = Student()
enrollment = Enrollment()
course = Course()

