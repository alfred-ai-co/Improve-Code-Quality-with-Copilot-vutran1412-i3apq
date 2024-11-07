from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional
from app.db_models.base import Ticket

class TicketCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[Ticket]:
        # Await the execute call to ensure the result is awaited.
        result = await self.db.execute(
            select(Ticket).offset(skip).limit(limit)
        )
        return result.scalars().all()  # scalars() is a method to get query results.

    async def create(self, **ticket_data) -> Ticket:
        # Create a new ticket and commit asynchronously.
        ticket = Ticket(**ticket_data)
        self.db.add(ticket)
        await self.db.commit()  # Await commit
        await self.db.refresh(ticket)  # Await refresh
        return ticket

    async def get(self, ticket_id: int) -> Optional[Ticket]:
        # Retrieve a ticket by ID.
        result = await self.db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalar_one_or_none()

    async def update(self, ticket_id: int, **ticket_data) -> Ticket:
        # Update a ticket by ID and commit.
        await self.db.execute(
            update(Ticket).where(Ticket.id == ticket_id).values(**ticket_data)
        )
        await self.db.commit()
        return await self.get(ticket_id)  # Return updated ticket

    async def delete(self, ticket_id: int) -> None:
        # Delete a ticket by ID and commit.
        await self.db.execute(delete(Ticket).where(Ticket.id == ticket_id))
        await self.db.commit()
