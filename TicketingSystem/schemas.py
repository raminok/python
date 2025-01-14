from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum

# Enum for Ticket Status
class TicketStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"

# Base model for ticket requests
class BaseTicketRequest(BaseModel):
    subject: str
    description: str

# Model for creating a ticket
class TicketRequest(BaseTicketRequest):
    user_id: Optional[int]

# Model for user-specific ticket requests
class TicketUserRequest(BaseModel):
    user_id: int

# Model for updating a ticket
class TicketUpdateRequest(BaseTicketRequest):
    ticket_id: int
    user_id: int
    status: TicketStatus

# Model for deleting a ticket
class TicketDeleteRequest(BaseModel):
    ticket_id: int

# Model for reassigning a ticket
class TicketReassignRequest(BaseModel):
    ticket_id: int
    new_user_id: int

# Model for fetching ticket history
class TicketHistoryRequest(BaseModel):
    ticket_id: int
    user_id: int

