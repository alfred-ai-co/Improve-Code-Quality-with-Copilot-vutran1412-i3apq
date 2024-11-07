import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_models.crud.ticket_crud import TicketCRUD
from app.db_models.base import Ticket
import datetime

@pytest.mark.anyio(anyio_backend="asyncio")
async def test_get_all_tickets(async_db_session: AsyncSession):
    """
    Test retrieving all tickets with default and custom pagination.
    """
    ticket_crud = TicketCRUD(async_db_session)

    # Create some test tickets
    for i in range(15):
        ticket = Ticket(
            title=f"Ticket {i}",
            description="Test",
            status="open",
            priority="low",
            project_id=1,
            kanban_status_id=1,
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )
        async_db_session.add(ticket)
    await async_db_session.commit()

    try:
        # Test default pagination
        tickets = await ticket_crud.get_all()
        assert len(tickets) == 10

        # Test custom pagination
        tickets = await ticket_crud.get_all(skip=5, limit=5)
        assert len(tickets) == 5
        assert tickets[0].title == "Ticket 5"
    except TimeoutError:
        pytest.fail("Database operation timed out")

@pytest.mark.anyio(anyio_backend="asyncio")
async def test_create_ticket(async_db_session: AsyncSession):
    """
    Test creating a new ticket.
    """
    ticket_crud = TicketCRUD(async_db_session)
    ticket_data = {
        "title": "Test Ticket",
        "description": "Test Description",
        "status": "open",
        "priority": "low",
        "project_id": 1,
        "kanban_status_id": 1,
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }
    try:
        ticket = await ticket_crud.create(**ticket_data)
        assert ticket.id is not None
        assert ticket.title == "Test Ticket"
    except TimeoutError:
        pytest.fail("Database operation timed out")

@pytest.mark.anyio(anyio_backend="asyncio")
async def test_get_ticket(async_db_session: AsyncSession):
    """
    Test retrieving a ticket by its ID.
    """
    ticket_crud = TicketCRUD(async_db_session)
    ticket_data = {
        "title": "Test Ticket",
        "description": "Test Description",
        "status": "open",
        "priority": "low",
        "project_id": 1,
        "kanban_status_id": 1,
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }
    ticket = await ticket_crud.create(**ticket_data)
    try:
        fetched_ticket = await ticket_crud.get(ticket.id)
        assert fetched_ticket.id == ticket.id
    except TimeoutError:
        pytest.fail("Database operation timed out")

@pytest.mark.anyio(anyio_backend="asyncio")
async def test_update_ticket(async_db_session: AsyncSession):
    """
    Test updating an existing ticket.
    """
    ticket_crud = TicketCRUD(async_db_session)
    ticket_data = {
        "title": "Test Ticket",
        "description": "Test Description",
        "status": "open",
        "priority": "low",
        "project_id": 1,
        "kanban_status_id": 1,
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }
    ticket = await ticket_crud.create(**ticket_data)
    try:
        updated_ticket = await ticket_crud.update(ticket.id, title="Updated Ticket")
        assert updated_ticket.title == "Updated Ticket"
    except TimeoutError:
        pytest.fail("Database operation timed out")

@pytest.mark.anyio(anyio_backend="asyncio")
async def test_delete_ticket(async_db_session: AsyncSession):
    """
    Test deleting a ticket by its ID.
    """
    ticket_crud = TicketCRUD(async_db_session)
    ticket_data = {
        "title": "Test Ticket",
        "description": "Test Description",
        "status": "open",
        "priority": "low",
        "project_id": 1,
        "kanban_status_id": 1,
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }
    ticket = await ticket_crud.create(**ticket_data)
    try:
        await ticket_crud.delete(ticket.id)
        assert await ticket_crud.get(ticket.id) is None
    except TimeoutError:
        pytest.fail("Database operation timed out")
