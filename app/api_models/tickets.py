from pydantic import BaseModel, Field
from typing import Optional, List
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

class TicketResponse(TicketCreate):
    """
    Schema for the response of a ticket.
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
