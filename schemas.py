from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

class Priority(PyEnum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class Status(PyEnum):
    Open = "Open"
    InProgress = "In Progress"
    Closed = "Closed"

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    tickets = relationship("Ticket", back_populates="user")

class Ticket(Base):
    __tablename__ = "ticket"
    ticket_id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255))
    description = Column(Text)
    status = Column(Enum(Status), default=Status.Open)
    priority = Column(Enum(Priority), default=Priority.Medium)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=True)
    user = relationship("User", back_populates="tickets")

class CreateTicketRequest(BaseModel):
    user_id: int
    subject: str
    description: str

class UpdateTicketRequest(BaseModel):
    ticket_id: int
    user_id: int
    subject: str
    description: str

class DeleteTicketRequest(BaseModel):
    ticket_id: int

class TicketResponse(BaseModel):
    ticket_id: int
    subject: str
    description: str
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
