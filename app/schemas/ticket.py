from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.history import HistoryEntry  # Corrected import statement

class TicketCreate(BaseModel):
    """
    Schema for creating a new ticket.
    """
    project_id: int
    title: str
    description: str
    status: str
    priority: str
    kanban_status_id: int  # Ensure this field is required

    def __repr__(self):
        return f"<TicketCreate(project_id={self.project_id}, title={self.title})>"


class Ticket(BaseModel):
    """
    Schema for representing a ticket.
    """
    id: int
    project_id: int
    title: str
    description: str
    status: str
    priority: str
    kanban_status_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    def __repr__(self):
        return f"<Ticket(id={self.id}, title={self.title})>"

class TicketResponse(Ticket):
    """
    Schema for the response of a ticket.
    """
    pass

class TicketWithHistory(BaseModel):
    """
    Schema for representing a ticket with its history.
    """
    ticket: TicketResponse
    history: List[HistoryEntry]

    class Config:
        orm_mode = True

    def __repr__(self):
        return f"<TicketWithHistory(ticket={self.ticket}, history_length={len(self.history)})>"
