###############################################
# Thicket Microservice for frontend           #
#                                             #
# Edit by : Ramin Orak 11/11/2024             #
###############################################
import httpx
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from schemas import TicketRequest, TicketUserRequest, TicketUpdateRequest, TicketDeleteRequest, TicketReassignRequest, TicketHistoryRequest
from utils import read_ticket, update_ticket, delete_ticket, assign_ticket, create_ticket, get_ticket_history, get_ticket_history_from_db, get_db 
import logging
from fastapi.exceptions import RequestValidationError
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

# Load environment settings from .env file
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("ticketapp.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load authentication information
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create FastAPI app
app = FastAPI(
    title="Ticket Management API",
    description="This API allows users to create, update, delete, and assign tickets.",
    version="1.0.0",
    docs_url="/documentation",
    redoc_url="/redoc",
)

# Add middleware to restrict access to trusted domains
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Endpoint to fetch tickets for a specific user
@app.get("/get_user_tickets")
async def get_user_tickets_endpoint(user: TicketUserRequest, page: int = 1, size: int = 10):
    try:
        data = user.dict()
        data.update({"page": page, "size": size})
        result = await read_ticket("get_user_tickets/", data, method="get")
        return result
    except Exception as e:
        logger.error(f"Error fetching user tickets: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to create a ticket
@app.post("/create_ticket")
async def create_ticket_endpoint(ticket: TicketRequest):
    try:
        data = ticket.dict()
        result = await create_ticket(data)
        return result
    except Exception as e:
        logger.error(f"Error creating ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to update a ticket
@app.put("/update_ticket")
async def update_ticket_endpoint(ticket: TicketUpdateRequest):
    try:
        data = ticket.dict()
        result = await update_ticket(data)
        return result
    except Exception as e:
        logger.error(f"Error updating ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to delete a ticket
@app.delete("/delete_ticket")
async def delete_ticket_endpoint(ticket: TicketDeleteRequest):
    try:
        data = ticket.dict()
        result = await delete_ticket(data)
        return result
    except Exception as e:
        logger.error(f"Error deleting ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to reassign a ticket to another user
@app.put("/assign_ticket")
async def reassign_ticket_endpoint(ticket: TicketReassignRequest):
    try: 
        data = ticket.dict()
        result = await assign_ticket(data)
        return result
    except Exception as e:
        logger.error(f"Error reassigning ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint for health check
@app.get("/health")
async def health_check():
    try:
        # Check connection to external services or database (if necessary)
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy"}

# Error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(httpx.HTTPStatusError)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=502,
        content={"detail": "External service error. Please try again later."},
    )

# Endpoint to get ticket history
@app.get("/get_ticket_history")
async def get_ticket_history(ticket_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the full conversation history for a specific ticket.
    """
 
    try:
        result=get_ticket_history_from_db(ticket_id, db)
        if not result:
            raise HTTPException(status_code=404, detail="Ticket history not found")
        
        return result
    except Exception as e:
        logger.error(f"Error fetching ticket history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the Ticket API")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the Ticket API")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
