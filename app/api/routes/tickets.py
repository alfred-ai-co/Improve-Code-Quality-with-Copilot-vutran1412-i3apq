from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from app.db_models.crud import TicketCRUD
from app.schemas.ticket import TicketCreate, TicketResponse
from app.api.dependencies.sqldb import get_db

router = APIRouter()

@router.post("/", status_code=201, response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """
    Create a new ticket.
    """
    ticket_crud = TicketCRUD(db)
    logger.info("Creating ticket with title: {}", ticket.title)
    if ticket.kanban_status_id is None:
        raise HTTPException(status_code=400, detail="kanban_status_id must be provided")
    try:
        return ticket_crud.create(**ticket.dict())
    except SQLAlchemyError as e:
        logger.error("Error creating ticket: {}", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", status_code=200, response_model=list[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    """
    Retrieve all tickets with pagination.
    """
    ticket_crud = TicketCRUD(db)
    logger.info("Fetching all tickets with skip: {} and limit: {}", skip, limit)
    try:
        return ticket_crud.get_all(skip=skip, limit=limit)
    except SQLAlchemyError as e:
        logger.error("Error fetching tickets: {}", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{id}", status_code=200, response_model=TicketResponse)
def get_ticket(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a ticket by its ID.
    """
    ticket_crud = TicketCRUD(db)
    try:
        ticket = ticket_crud.get(id)
        if not ticket:
            logger.error("Ticket with id {} not found", id)
            raise HTTPException(status_code=404, detail=f"Ticket with id {id} not found")
        logger.info("Fetching ticket with id: {}", id)
        return ticket
    except SQLAlchemyError as e:
        logger.error("Error fetching ticket: {}", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{id}", status_code=200, response_model=TicketResponse)
def update_ticket(id: int, ticket: TicketCreate, db: Session = Depends(get_db)):
    """
    Update an existing ticket.
    """
    ticket_crud = TicketCRUD(db)
    logger.info("Updating ticket with id: {}", id)
    try:
        ticket_crud.update(id, **ticket.dict())
        return ticket_crud.get(id)
    except SQLAlchemyError as e:
        logger.error("Error updating ticket: {}", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{id}", status_code=204)
async def delete_ticket(id: int, db: Session = Depends(get_db)):
    """
    Delete a ticket by its ID.
    """
    ticket_crud = TicketCRUD(db)
    logger.info("Deleting ticket with id: {}", id)
    try:
        ticket_crud.delete(id)
        return {"message": "Ticket deleted successfully"}
    except SQLAlchemyError as e:
        logger.error("Error deleting ticket: {}", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")
