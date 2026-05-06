from app.models.Base import Base
from sqlalchemy import Integer, String, Column, Text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable = False, unique=True)
    hashed_password = Column(String, nullable=False)
    
    tasks = relationship("Task", back_populates="user")