from pydantic import BaseModel
from datetime import datetime

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
        orm_mode: True

class TicketResponse(Ticket):
    """
    Schema for the response of a ticket.
    """
    pass
