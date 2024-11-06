from pydantic import BaseModel
from datetime import datetime

class TicketCreate(BaseModel):
    project_id: int
    title: str
    description: str
    status: str
    priority: str
    kanban_status_id: int  # Ensure this field is required

class Ticket(BaseModel):
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
    pass
