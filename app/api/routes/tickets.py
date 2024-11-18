from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from app.db_models.crud import TicketCRUD
from app.db_models.crud.history_crud import HistoryCRUD
from app.schemas.ticket import TicketCreate, TicketResponse, TicketWithHistory
from app.api.dependencies.sqldb import get_db
from app.services.ticket_service import update_ticket_status

router = APIRouter()

@router.post("/", status_code=201, response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)) -> TicketResponse:
    """
    Create a new ticket.
    """
    ticket_crud = TicketCRUD(db)
    logger.info("Creating ticket with title: {}", ticket.title)
    if ticket.kanban_status_id is None:
        raise HTTPException(status_code=400, detail="kanban_status_id must be provided")
    try:
        return ticket_crud.create(**ticket.model_dump())
    except SQLAlchemyError as e:
        logger.error("Error creating ticket: {}", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", status_code=200, response_model=list[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db), skip: int = 0, limit: int = 10) -> list[TicketResponse]:
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
def get_ticket(id: int, db: Session = Depends(get_db)) -> TicketResponse:
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

@router.get("/{id}/history", response_model=TicketWithHistory)
def get_ticket_with_history(id: int, db: Session = Depends(get_db)) -> TicketWithHistory:
    """
    Retrieve a ticket along with its history by its ID.
    """
    ticket_crud = TicketCRUD(db)
    history_crud = HistoryCRUD(db)

    logger.info("Fetching ticket with history for id: {}", id)
    ticket = ticket_crud.get(id)
    if not ticket:
        logger.error("Ticket with id {} not found", id)
        raise HTTPException(status_code=404, detail="Ticket not found")

    history = history_crud.get_by_entity_id('ticket', id)

    return {"ticket": ticket, "history": history}

@router.put("/{id}", status_code=200, response_model=TicketResponse)
def update_ticket(id: int, ticket: TicketCreate, db: Session = Depends(get_db)) -> TicketResponse:
    """
    Update an existing ticket.
    """
    ticket_crud = TicketCRUD(db)
    logger.info("Updating ticket with id: {}", id)
    try:
        ticket_crud.update(id, **ticket.model_dump())
        return ticket_crud.get(id)
    except SQLAlchemyError as e:
        logger.error("Error updating ticket: {}", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{ticket_id}/status", response_model=TicketResponse)
def change_ticket_status(ticket_id: int, new_status: str, user_id: int, db: Session = Depends(get_db)) -> TicketResponse:
    """
    Change the status of an existing ticket.
    """
    logger.info("Changing status of ticket with id: {} to {}", ticket_id, new_status)
    try:
        ticket = update_ticket_status(ticket_id, new_status, user_id, db)
        return ticket
    except ValueError as e:
        logger.error("Error changing ticket status: {}", str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error: {}", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{id}", status_code=204)
def delete_ticket(id: int, db: Session = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    ticket = ticket_crud.get(id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket_crud.delete(id)
    return None  # Ensure no response body is returned
