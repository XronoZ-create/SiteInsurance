from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database_email import Base, SessionLocal
import random

class Email(Base):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)

    email_address = Column(String)
    email_password = Column(String)

    user_id = Column(String)