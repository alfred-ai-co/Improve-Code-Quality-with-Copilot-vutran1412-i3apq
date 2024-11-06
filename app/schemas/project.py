from pydantic import BaseModel
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: str
    kanban_board_id: int  # Ensure this field is required

class Project(BaseModel):
    id: int
    name: str
    description: str
    kanban_board_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode: True

class ProjectResponse(Project):
    pass
