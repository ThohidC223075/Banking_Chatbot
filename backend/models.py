from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, Integer, String
from database import Base
# Login schema
class LoginForm(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

# Signup schema
class SignupForm(BaseModel):  # ✅ fixed class name
    email: EmailStr
    password: str = Field(..., min_length=6)

# Chatbot schema
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    
class User(Base):
    __tablename__ = "users"  # must match the real table name in DB

    
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, index=True)