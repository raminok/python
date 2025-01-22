# This is a middleware function scripts for business layer of ticketing system

from database import DATABASE_CONFIG
from fastapi import HTTPException
from sqlalchemy.orm import Session
import httpx
import logging

logger = logging.getLogger(__name__)

# Read Ticket API   
async def read_ticket(data: dict):
    url = f"{DATABASE_CONFIG['api_url']}read"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error occurred: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Create Ticket API
async def create_ticket(data: dict):
    url = f"{DATABASE_CONFIG['api_url']}create"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error occurred: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Delete Ticket API
async def delete_ticket(data: dict):
    url = f"{DATABASE_CONFIG['api_url']}delete"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error occurred: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Update Ticket API
async def update_ticket(data: dict):
    url = f"{DATABASE_CONFIG['api_url']}update"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error occurred: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# give full conversation for each ticket
async def get_ticket_history_from_db(ticket_id: int, db: Session):
    try:
        ticket_history = db.query(TicketHistory).filter(TicketHistory.ticket_id == ticket_id).all()
        if not ticket_history:
            raise HTTPException(status_code=404, detail="Ticket history not found")
        return ticket_history

    except Exception as e:
        logger.error(f"Error occurred while fetching ticket history: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")

# Assign Ticket API
async def assign_ticket(data: dict):
    url = f"{DATABASE_CONFIG['api_url']}assign"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error occurred: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
