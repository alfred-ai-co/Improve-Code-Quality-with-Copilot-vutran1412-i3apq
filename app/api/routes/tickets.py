from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from loguru import logger

from app.db_models.crud import TicketCRUD
from app.schemas.ticket import TicketCreate, TicketResponse
from app.api.dependencies.sqldb import get_db

router = APIRouter()

@router.post("/", status_code=201, response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    logger.info("Creating ticket with title: {}", ticket.title)
    if ticket.kanban_status_id is None:
        raise HTTPException(status_code=400, detail="kanban_status_id must be provided")
    return ticket_crud.create(**ticket.dict())

@router.get("/", status_code=200, response_model=list[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    ticket_crud = TicketCRUD(db)
    logger.info("Fetching all tickets with skip: {} and limit: {}", skip, limit)
    return ticket_crud.get_all(skip=skip, limit=limit)

@router.get("/{id}", status_code=200, response_model=TicketResponse)
def get_ticket(id: int, db: Session = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    ticket = ticket_crud.get(id)
    if not ticket:
        logger.error("Ticket with id {} not found", id)
        raise HTTPException(status_code=404, detail=f"Ticket with id {id} not found")
    logger.info("Fetching ticket with id: {}", id)
    return ticket

@router.put("/{id}", status_code=200, response_model=TicketResponse)
def update_ticket(id: int, ticket: TicketCreate, db: Session = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    logger.info("Updating ticket with id: {}", id)
    ticket_crud.update(id, **ticket.dict())
    return ticket_crud.get(id)

@router.delete("/{id}", status_code=204)
async def delete_ticket(id: int, db: Session = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    logger.info("Deleting ticket with id: {}", id)
    ticket_crud.delete(id)
    return {"message": "Ticket deleted successfully"}
