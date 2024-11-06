import pytest
from sqlalchemy.orm import Session
from app.db_models.crud.ticket_crud import TicketCRUD
from app.db_models.base import Ticket

def test_get_all_tickets(db_session: Session):
    ticket_crud = TicketCRUD(db_session)

    # Create some test tickets
    for i in range(15):
        ticket = Ticket(title=f"Ticket {i}", description="Test", status="open", priority="low", project_id=1, kanban_status_id=1)
        db_session.add(ticket)
    db_session.commit()

    # Test default pagination
    tickets = ticket_crud.get_all()
    assert len(tickets) == 10

    # Test custom pagination
    tickets = ticket_crud.get_all(skip=5, limit=5)
    assert len(tickets) == 5
    assert tickets[0].title == "Ticket 5"

def test_create_ticket(db_session: Session):
    ticket_crud = TicketCRUD(db_session)
    ticket_data = {"title": "Test Ticket", "description": "Test Description", "status": "open", "priority": "low", "project_id": 1, "kanban_status_id": 1}
    ticket = ticket_crud.create(**ticket_data)
    assert ticket.id is not None
    assert ticket.title == "Test Ticket"

def test_get_ticket(db_session: Session):
    ticket_crud = TicketCRUD(db_session)
    ticket_data = {"title": "Test Ticket", "description": "Test Description", "status": "open", "priority": "low", "project_id": 1, "kanban_status_id": 1}
    ticket = ticket_crud.create(**ticket_data)
    fetched_ticket = ticket_crud.get(ticket.id)
    assert fetched_ticket.id == ticket.id

def test_update_ticket(db_session: Session):
    ticket_crud = TicketCRUD(db_session)
    ticket_data = {"title": "Test Ticket", "description": "Test Description", "status": "open", "priority": "low", "project_id": 1, "kanban_status_id": 1}
    ticket = ticket_crud.create(**ticket_data)
    updated_ticket = ticket_crud.update(ticket.id, title="Updated Ticket")
    assert updated_ticket.title == "Updated Ticket"

def test_delete_ticket(db_session: Session):
    ticket_crud = TicketCRUD(db_session)
    ticket_data = {"title": "Test Ticket", "description": "Test Description", "status": "open", "priority": "low", "project_id": 1, "kanban_status_id": 1}
    ticket = ticket_crud.create(**ticket_data)
    ticket_crud.delete(ticket.id)
    assert ticket_crud.get(ticket.id) is None
