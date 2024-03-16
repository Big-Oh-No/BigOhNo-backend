from ..utils.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Enum, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
import enum




class Dept(enum.Enum):
    cosc = "COSC"
    phys = "PHYS"
    bio = "BIO"
    chem = "CHEM"
    math = "MATH"
    data = "DATA"
    stat = "STAT"

class Term(enum.Enum):
    w_one = "W1"
    w_two = "W2"
    s_one = "S1"
    s_two = "S2"

    
   
class Status(enum.Enum):
    approved = "approved"
    declined = "declined"
    pending = "pending"


  
    
class Enrollment(Base):
    __tablename__ = "enrollment"
    comment = Column(String)
    status = Column(Enum(Status))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    
class Course(Base):
     __tablename__ = "course"
     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
     dept = Column(Enum(Dept), nullable=False)
     code = Column(Integer, nullable=False) 
     name = Column(String, nullable=False) 
     description = Column(String)
     syslabus_url = Column(String)
     term = Column(Enum(Term), nullable=False)
     year = Column(Integer, nullable=False) 
     credits = Column(Integer, nullable=False) 
     total_seats = Column(Integer, nullable=False)
     taken_seats = Column(Integer, server_default=0)
     status = Column(Enum(Status))
     
         
     
     
     
     
     
     
     
    
    
    
    