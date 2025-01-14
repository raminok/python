from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from services.ticket_service import create_ticket, get_tickets, get_ticket_or_404, update_ticket, delete_ticket
from pydantic import BaseModel
import logging
from datetime import datetime

# تنظیمات لاگ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger(__name__)

router = APIRouter()

# مدل‌های درخواست و پاسخ
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

# ایجاد یک تیکت
@router.post("/tickets", response_model=TicketResponse)
def create_ticket_endpoint(request: CreateTicketRequest, db: Session = Depends(get_db)):
    try:
        ticket = create_ticket(db, user_id=request.user_id, subject=request.subject, description=request.description)
        logger.info(f"Ticket created successfully: {ticket.ticket_id}")
        return ticket
    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error creating ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# بررسی وضعیت تیکت و به‌روزرسانی آن
@router.put("/tickets", response_model=TicketResponse)
def update_ticket_endpoint(request: UpdateTicketRequest, db: Session = Depends(get_db)):
    try:
        ticket = get_ticket_or_404(db, request.ticket_id)
        if ticket.status == "Closed":
           ticket.status = "In Progress"
           logger.info(f"Ticket {ticket.ticket_id} reopened and set to 'In Progress'.")

        updated_ticket = update_ticket(db,
           ticket_id=request.ticket_id,
           user_id=request.user_id,
           subject=request.subject,
           description=request.description,
           status=ticket.status)
        
        logger.info(f"Ticket updated successfully: {updated_ticket.ticket_id}")
        return updated_ticket
    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error updating ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# حذف تیکت
@router.post("/tickets/delete")
def delete_ticket_endpoint(request: DeleteTicketRequest, db: Session = Depends(get_db)):
    try:
        ticket = get_ticket_or_404(db, request.ticket_id)
        success = delete_ticket(db, request.ticket_id)
        if success:
            logger.info(f"Ticket deleted successfully: {request.ticket_id}")
            return {"message": "Ticket deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# مشاهده تمام تیکت‌ها
@router.get("/tickets", response_model=list[TicketResponse])
def get_all_tickets_endpoint(db: Session = Depends(get_db)):
    try:
        tickets = get_tickets(db)
        logger.info("All tickets retrieved successfully.")
        return tickets
    except Exception as e:
        logger.error(f"Error retrieving tickets: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
